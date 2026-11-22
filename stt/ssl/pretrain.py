"""SSL pretraining entry (Phase 3).

Usage:
  torchrun --standalone --nproc_per_node=<N> -m stt.ssl.pretrain --config configs/stt/ssl_hubert.yaml

Features (filled Phase 3):
- wav2vec 2.1 or HuBERT loop (ADR-02 addendum: variant decision).
- Masking (time), EMA, momentum update (wav2vec2), contrastive/cluster losses.
- Checkpoints -> artifacts/ssl/<name>/latest.pth
- Phoneme probe eval (stt/ssl/eval_phoneme.py) at eval cadence.
"""

from __future__ import annotations

import argparse

import torch

from shared.config_util import load_config
from stt.ssl.dataset import SSLManifestDataset


def main() -> None:
    ap = argparse.ArgumentParser(description="SSL pretraining (Phase 3).")
    ap.add_argument("--config", default="configs/stt/ssl_hubert.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)

    # Skeleton: choose SSL variant per ADR-02 addendum, build dataset/loader,
    # mask, compute loss, backward, EMA, checkpoint.
    print(f"[Phase 3 skeleton] config: {cfg}")
    print("Real SSL pretraining loop starts Phase 3.")
    ds = SSLManifestDataset("data/manifests/train.jsonl")
    print(f"dataset entries: {len(ds)}")


if __name__ == "__main__":
    main()
