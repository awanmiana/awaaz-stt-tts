"""FastConformer-style encoder (Phase 0 skeleton; filled in Phase 2/4).

Structure:
- ConvSubsampling (8x time downsample)
- Stack of ConformerBlocks (rel-pos MHA + depthwise conv + pointwise FFN)

From scratch: relative positional encoding, depthwise conv module,
SpecAugment hooks at train time (configs/stt/*.yaml).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class FastConformerConfig:
    d_model: int = 128
    n_layers: int = 8
    n_heads: int = 4
    subsample_factor: int = 8
    dropout: float = 0.1
    conv_kernel_size: int = 9


class ConvSubsampling(nn.Module):
    """Stacked strided Conv2d subsampling (FastConformer style, ~8x)."""

    def __init__(self, feat_dim: int, d_model: int, subsample_factor: int = 8):
        super().__init__()
        self.subsample_factor = subsample_factor
        n_stages = max(1, int(round(math.log2(subsample_factor))))
        layers = []
        cin = 1
        for i in range(n_stages):
            cout = d_model if i > 0 else d_model
            layers += [
                nn.Conv2d(cin, cout, kernel_size=3, stride=2, padding=1),
                nn.BatchNorm2d(cout),
                nn.ReLU(),
            ]
            cin = cout
        self.conv = nn.Sequential(*layers)
        self.proj = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, F] -> [B, T', d_model]
        x = x.unsqueeze(1)
        x = self.conv(x)
        b, d, t, f = x.shape
        x = x.permute(0, 2, 1, 3).reshape(b, t, d * f)
        return self.proj(x)


class RelPositionalEncoding(nn.Module):
    """Sinusoidal relative positional encoding (simplified)."""

    def __init__(self, d_model: int, max_len: int = 4096):
        super().__init__()
        self.d_model = d_model
        self.max_len = max_len
        self.register_buffer("pe", self._build(max_len))

    def _build(self, max_len: int) -> torch.Tensor:
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, self.d_model, 2).float() * (-math.log(10000.0) / self.d_model))
        pe = torch.zeros(max_len, self.d_model)
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        return pe

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        t = x.shape[1]
        return x + self.pe[:t].unsqueeze(0)


class RelativeMHSA(nn.Module):
    """Multi-head self-attention with relative positional embeddings (skeleton)."""

    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.n_heads = n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.rel_pos = RelPositionalEncoding(d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, d = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q = q.view(b, t, self.n_heads, -1).transpose(1, 2)
        k = k.view(b, t, self.n_heads, -1).transpose(1, 2)
        v = v.view(b, t, self.n_heads, -1).transpose(1, 2)
        scale = math.sqrt(d // self.n_heads)
        attn = torch.softmax((q @ k.transpose(-2, -1)) / scale, dim=-1)
        out = (attn @ v).transpose(1, 2).reshape(b, t, d)
        return self.out(out)


class DepthwiseConvModule(nn.Module):
    """Depthwise-separable conv module (simplified)."""

    def __init__(self, d_model: int, kernel: int = 9):
        super().__init__()
        self.dw = nn.Conv1d(d_model, d_model, kernel, padding=kernel // 2, groups=d_model)
        self.pw = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.transpose(1, 2)
        x = self.dw(x)
        x = F.relu(x)
        x = x.transpose(1, 2)
        return self.pw(x)


class ConformerBlock(nn.Module):
    """MHSA + conv module + FFN (standard post-norm simplification)."""

    def __init__(self, d_model: int, n_heads: int, conv_kernel: int = 9, dropout: float = 0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attn = RelativeMHSA(d_model, n_heads)
        self.norm2 = nn.LayerNorm(d_model)
        self.conv = DepthwiseConvModule(d_model, conv_kernel)
        self.norm3 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(4 * d_model, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.norm1(x))
        x = x + self.conv(self.norm2(x))
        x = x + self.ffn(self.norm3(x))
        return x


class FastConformerEncoder(nn.Module):
    def __init__(self, cfg: FastConformerConfig, n_mels: int = 80):
        super().__init__()
        self.cfg = cfg
        self.subsample = ConvSubsampling(n_mels, cfg.d_model, cfg.subsample_factor)
        self.pos = RelPositionalEncoding(cfg.d_model)
        self.blocks = nn.ModuleList(
            [ConformerBlock(cfg.d_model, cfg.n_heads, cfg.conv_kernel_size, cfg.dropout) for _ in range(cfg.n_layers)]
        )
        self.norm = nn.LayerNorm(cfg.d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, n_mels]
        x = self.subsample(x)
        x = self.pos(x)
        for blk in self.blocks:
            x = blk(x)
        return self.norm(x)


class FastConformerCTC(nn.Module):
    """Encoder + CTC head (primary decoder; RNN-T variant in stt/model/rnnt.py)."""

    def __init__(self, cfg: FastConformerConfig, n_mels: int = 80, vocab_size: int = 64):
        super().__init__()
        self.encoder = FastConformerEncoder(cfg, n_mels)
        self.ctc_head = nn.Linear(cfg.d_model, vocab_size)
        self.blank_id = 0  # index 0 reserved as CTC blank

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        enc = self.encoder(x)
        return self.ctc_head(enc)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    cfg = FastConformerConfig()
    model = FastConformerCTC(cfg, vocab_size=64)
    feats = torch.randn(2, 100, 80)
    logits = model(feats)
    print("encoder out:", model.encoder(feats).shape, "ctc logits:", logits.shape)
