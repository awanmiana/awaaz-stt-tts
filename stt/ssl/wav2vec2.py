"""Wav2Vec 2.1-style contrastive SSL pretraining (Phase 0 skeleton; filled Phase 3).

Components:
- FeatureEncoder: Conv2d stack (waveform -> latents, ~20ms hop)
- TransformerEncoder: relative-pos MHSA + conv module (from FastConformer building blocks)
- GumbelVectorQuantizer: groups x vars quantization (contrastive targets)
- Loss: contrastive + diversity — filled Phase 3.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class Wav2Vec2Config:
    encoder_dim: int = 256
    encoder_layers: int = 6
    num_groups: int = 2
    num_vars: int = 320
    latent_dim: int = 128
    feat_extract_dim: int = 512


class FeatureEncoder(nn.Module):
    def __init__(self, feat_extract_dim: int = 512, out_dim: int = 256):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(1, feat_extract_dim, 5, stride=2, padding=2), nn.GroupNorm(8, feat_extract_dim), nn.ReLU(),
            nn.Conv1d(feat_extract_dim, feat_extract_dim, 5, stride=2, padding=2), nn.GroupNorm(8, feat_extract_dim), nn.ReLU(),
            nn.Conv1d(feat_extract_dim, out_dim, 5, stride=2, padding=2), nn.GroupNorm(8, out_dim), nn.ReLU(),
        )

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        # waveform: [B, T] -> latents [B, T', D]
        x = waveform.unsqueeze(1)
        return self.conv(x).transpose(1, 2)


class TransformerEncoder(nn.Module):
    def __init__(self, d_model: int = 256, n_layers: int = 6, n_heads: int = 4):
        super().__init__()
        from stt.model.fastconformer import ConformerBlock

        self.blocks = nn.ModuleList([ConformerBlock(d_model, n_heads) for _ in range(n_layers)])
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for blk in self.blocks:
            x = blk(x)
        return self.norm(x)


class GumbelVectorQuantizer(nn.Module):
    def __init__(self, latent_dim: int = 128, num_groups: int = 2, num_vars: int = 320):
        super().__init__()
        self.num_groups = num_groups
        self.num_vars = num_vars
        self.codevecs = nn.ParameterList([nn.Parameter(torch.randn(num_vars, latent_dim // num_groups)) for _ in range(num_groups)])

    def forward(self, x: torch.Tensor, temp: float = 2.0):  # pragma: no cover - Phase 3
        raise NotImplementedError("Wav2Vec2 contrastive loss details filled Phase 3.")


class Wav2Vec2(nn.Module):
    def __init__(self, cfg: Wav2Vec2Config):
        super().__init__()
        self.cfg = cfg
        self.feature_extractor = FeatureEncoder(cfg.feat_extract_dim, cfg.encoder_dim)
        self.quantizer = GumbelVectorQuantizer(cfg.latent_dim, cfg.num_groups, cfg.num_vars)
        self.encoder = TransformerEncoder(cfg.encoder_dim, cfg.encoder_layers)

    def forward(self, waveform: torch.Tensor, mask: bool = True):  # pragma: no cover - Phase 3
        latents = self.feature_extractor(waveform)
        return self.encoder(latents)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    m = Wav2Vec2(Wav2Vec2Config())
    print("feats:", m.feature_extractor(torch.randn(2, 16000)).shape)
    print("enc:", m.encoder(torch.randn(2, 100, 256)).shape)
