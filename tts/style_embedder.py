"""Style embedder (Phase 0 skeleton; style system trained in Phase 6).

Two components:
- StyleTagEmbedding: learned per-tag embeddings (from configs/tts defaults + pack style variants).
- ContinuousStyleEncoder: maps style features (pace/pitch/timbre contours) -> style vector.
- StyleClassifier: style vector -> class logits (for evaluation; trained Phase 6).
"""

from __future__ import annotations

import torch
import torch.nn as nn

from shared.constants import STYLES


class StyleTagEmbedding(nn.Module):
    def __init__(self, style_dim: int = 32, vocab: list[str] | None = None):
        super().__init__()
        self.vocab = vocab or list(STYLES)
        self.table = nn.Embedding(len(self.vocab), style_dim)

    def forward(self, idx: torch.Tensor) -> torch.Tensor:
        return self.table(idx)


class ContinuousStyleEncoder(nn.Module):
    def __init__(self, in_dim: int = 8, style_dim: int = 32):
        super().__init__()
        self.mlp = nn.Sequential(nn.Linear(in_dim, 64), nn.ReLU(), nn.Linear(64, style_dim))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.mlp(features)


class StyleClassifier(nn.Module):
    def __init__(self, style_dim: int = 32, n_classes: int | None = None):
        super().__init__()
        self.n_classes = n_classes or len(STYLES)
        self.head = nn.Linear(style_dim, self.n_classes)

    def forward(self, style_vec: torch.Tensor) -> torch.Tensor:
        return self.head(style_vec)


if __name__ == "__main__":  # pragma: no cover
    torch.manual_seed(0)
    e = StyleTagEmbedding()
    print("tag emb:", e(torch.tensor([0, 1])).shape)
