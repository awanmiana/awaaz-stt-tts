"""Codec decoder: latents -> waveform (HiFi-Gan-ish, Phase 0; filled Phase 5).

Target: reconstruct speech waveform from RVQ latents.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class ConvDecoder(nn.Module):
    def __init__(self, latent_dim: int = 64, mel_dim: int = 80, ups: tuple = (4, 4, 2)):
        super().__init__()
        layers: list[nn.Module] = []
        cin = latent_dim
        for u in ups:
            cout = max(cin // 4, 32)
            layers += [nn.ConvTranspose1d(cin, cout, u, stride=u, padding=0), nn.ReLU()]
            cin = cout
        layers += [nn.Conv1d(cin, mel_dim, 7, padding=3), nn.ReLU()]
        self.dec = nn.Sequential(*layers)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        # z: [B, D, T'] -> mel: [B, T, F]
        return self.dec(z).transpose(1, 2)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    dec = ConvDecoder()
    x = dec(torch.randn(2, 64, 10))
    print("out:", x.shape)
