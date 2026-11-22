"""Cosine similarity utilities for speaker/embedding evaluation (Phase 0)."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(a @ b / (na * nb))


def mean_pairwise_speaker_similarity(embeddings: Sequence[Sequence[float]]) -> float:
    embs = [np.asarray(e, dtype=np.float32) for e in embeddings]
    if not embs:
        return 0.0
    sims = [cosine_similarity(embs[i], embs[j]) for i in range(len(embs)) for j in range(i + 1, len(embs))]
    return float(np.mean(sims)) if sims else 0.0


if __name__ == "__main__":  # pragma: no cover
    print(cosine_similarity([1, 0], [1, 0]), cosine_similarity([1, 0], [0, 1]))
