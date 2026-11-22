"""Speaker encoder — ECAPA-TDNN-class skeleton (Phase 5: from scratch).

Takes mel spectrogram(s) -> L2-normalized speaker embedding (default 192-d).
Train via speaker-verification loss (triplet/AAM-softmax), from scratch.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class SpeakerEncoder(nn.Module):
    def __init__(self, mel_dim: int = 80, emb_dim: int = 192):
        super().__init__()
        self.blocks = nn.Sequential(
            nn.Conv1d(mel_dim, 256, 5, padding=2), nn.ReLU(),
            nn.Conv1d(256, 256, 5, padding=2), nn.ReLU(),
            nn.Conv1d(256, 512, 5, padding=2), nn.ReLU(),
        )
        self.mean_pool = nn.AdaptiveAvgPool1d(1)
        self.head = nn.Linear(512, emb_dim)

    def forward(self, mel: torch.Tensor) -> torch.Tensor:
        # mel: [B, T, F] -> emb: [B, emb_dim]
        x = self.blocks(mel.transpose(1, 2))
        x = self.mean_pool(x).squeeze(-1)
        return F.normalize(self.head(x), dim=-1)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    enc = SpeakerEncoder()
    print("emb:", enc(torch.randn(2, 100, 80)).shape)
