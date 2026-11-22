"""Codec encoder: mel/wav -> latent sequence at codec frame rate (Phase 0; filled Phase 5).

Target: ~12.5 tokens/sec (80ms frames); 8 codebooks x 1024 entries per frame.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class ConvEncoder(nn.Module):
    def __init__(self, mel_dim: int = 80, latent_dim: int = 64, hidden: int = 256):
        super().__init__()
        convs = []
        cin = mel_dim
        for c in (hidden, hidden * 2, latent_dim):
            convs += [nn.Conv1d(cin, c, 5, padding=2), nn.ReLU(), nn.Conv1d(c, c, 5, padding=2), nn.ReLU()]
            cin = c
        self.enc = nn.Sequential(*convs)
        self.norm = nn.LayerNorm(latent_dim)

    def forward(self, mel: torch.Tensor) -> torch.Tensor:
        # mel: [B, T, F] -> latents: [B, D, T']
        x = self.enc(mel.transpose(1, 2))
        return self.norm(x.transpose(1, 2)).transpose(1, 2)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    enc = ConvEncoder()
    z = enc(torch.randn(2, 100, 80))
    print("latents:", z.shape)
