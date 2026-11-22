"""TTS evaluation entry (Phase 6 targets; skeleton now).

Metrics (filled in Phase 6):
- UTMOS (automated naturalness; see eval/benchmarks/README.md)
- Speaker similarity vs. enrollment embedding
- Style accuracy (classifier; tts/style_embedder.StyleClassifier)
- Speed/pitch control checks
"""

from __future__ import annotations

import argparse

import numpy as np

from eval.speaker_similarity import cosine_similarity
from shared.config_util import load_config


def print_report(metrics: dict[str, float]):
    print("metric | value")
    print("-" * 40)
    for k, v in metrics.items():
        print(f"{k} | {v:.3f}" if isinstance(v, float) else f"{k} | {v}")


def main():
    ap = argparse.ArgumentParser(description="Evaluate TTS (skeleton; Phase 6).")
    ap.add_argument("--config", default="configs/tts/default.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)["tts"]

    metrics = {
        "utmos": float("nan"),
        "speaker_sim_avg": 0.0,
        "style_acc": float("nan"),
        "pitch_std_ok": True,
        "speed_ratio": cfg["defaults"]["speed"],
    }
    print("[Phase 0] TTS skeleton eval. Real metrics after Phase 6 training.")
    print_report({k: v for k, v in metrics.items() if not isinstance(v, float) or v == v})
    _ = cosine_similarity([1, 0], [1, 0])
    _ = np.zeros(1)


if __name__ == "__main__":
    main()
