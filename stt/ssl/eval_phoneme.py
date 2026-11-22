"""Linear phoneme-discrimination probe eval (Phase 3 gate).

Method (filled Phase 3):
- Dump frozen SSL latents for held-out set.
- Use forced-alignment frames (data/scripts/forced_align.py, Phase 5 tooling)
  to assign latent frames -> phoneme IDs (from shared/phoneme_inventory.py).
- Train linear probe on (latent frames, phoneme IDs); report per-phoneme recall.

Gate (docs/phase3_ssl.md): per-phoneme recall ≥ 50% on held-out set.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from shared.phoneme_inventory import PHONEMES


def frame_phoneme_recall_report(y_true: list[int], y_pred: list[int]) -> dict[str, Any]:
    """Per-class recall on frame-level phone IDs (skeleton; real pipeline Phase 3)."""
    recall: dict[str, float] = {}
    for ph in range(len(PHONEMES)):
        t = [i for i, t in enumerate(y_true) if t == ph]
        if not t:
            recall[PHONEMES[ph]] = 0.0
            continue
        correct = sum(1 for i in t if y_pred[i] == ph)
        recall[PHONEMES[ph]] = correct / len(t)
    return {"mean_recall": float(np.mean([recall[p] for p in recall])), "per_phoneme": recall}


if __name__ == "__main__":  # pragma: no cover
    rep = frame_phoneme_recall_report([0, 0, 1, 1, 2], [0, 1, 1, 1, 2])
    print(rep)
