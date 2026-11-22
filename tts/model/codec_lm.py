"""Codec-LM (CosyVoice-class generative model, Phase 0 skeleton; trained Phase 6).

Text (Urdu, phoneme-ids) + speaker embedding + style embedding
    -> transformer -> per-frame speech-token logits (8 codebooks x 1024).
Streaming-capable (KV cache design note; implemented Phase 7/8).
"""

from __future__ import annotations

import torch
import torch.nn as nn

from shared.phoneme_inventory import N_PHONEMES


class CodecBlock(nn.Module):
    """Transformer block (MHSA + FFN) — compact skeleton."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        self.n_heads = n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out = nn.Linear(d_model, d_model)
        self.ffn = nn.Sequential(nn.Linear(d_model, 4 * d_model), nn.GELU(), nn.Linear(4 * d_model, d_model))
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor, causal: bool = True) -> torch.Tensor:
        b, t, d = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q = q.view(b, t, self.n_heads, -1).transpose(1, 2)
        k = k.view(b, t, self.n_heads, -1).transpose(1, 2)
        v = v.view(b, t, self.n_heads, -1).transpose(1, 2)
        import math

        attn = q @ k.transpose(-2, -1) / math.sqrt(d // self.n_heads)
        if causal:
            mask = torch.triu(torch.ones(t, t, device=x.device, dtype=torch.bool), diagonal=1)
            attn = attn.masked_fill(mask, float("-inf"))
        attn = torch.softmax(attn, dim=-1)
        x = x + self.out((attn @ v).transpose(1, 2).reshape(b, t, d))
        x = self.norm(x + self.ffn(x))
        return x


class CodecLM(nn.Module):
    def __init__(self, vocab_size: int = 8192, d_model: int = 384, n_layers: int = 12, n_heads: int = 8,
                 speaker_dim: int = 192, style_dim: int = 32, text_vocab: int | None = None):
        super().__init__()
        self.text_emb = nn.Embedding(text_vocab or (N_PHONEMES + 8), d_model)
        self.speaker_proj = nn.Linear(speaker_dim, d_model)
        self.style_proj = nn.Linear(style_dim, d_model)
        self.blocks = nn.ModuleList([CodecBlock(d_model, n_heads) for _ in range(n_layers)])
        self.head = nn.Linear(d_model, vocab_size)
        self.d_model = d_model

    def forward(self, text_ids: torch.Tensor, speaker_emb: torch.Tensor, style_emb: torch.Tensor,
                speech_prefix: torch.Tensor | None = None) -> torch.Tensor:
        """Returns logits: [B, T, vocab_size] predicting next speech token (teacher forcing)."""
        x = self.text_emb(text_ids) + self.speaker_proj(speaker_emb).unsqueeze(1) + self.style_proj(style_emb).unsqueeze(1)
        for blk in self.blocks:
            x = blk(x)
        return self.head(x)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    m = CodecLM()
    text_ids = torch.zeros(2, 10, dtype=torch.long)
    spk = torch.randn(2, 192)
    style = torch.randn(2, 32)
    logits = m(text_ids, spk, style)
    print("logits:", logits.shape)
