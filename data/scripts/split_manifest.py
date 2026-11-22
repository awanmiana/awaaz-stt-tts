"""Split a manifest into train/dev/test (Phase 1).

Usage:
  python -m data.scripts.split_manifest --manifest data/manifests/train.jsonl --out-dir data/manifests
                                        [--train-ratio 0.9 --dev-ratio 0.05 --seed 42 --out-prefix corpus]

Random split with seed; emits `<out-dir>/<out-prefix>_train.jsonl` etc.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from shared.manifest import load_manifest, save_manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="Split a manifest into train/dev/test.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-dir", default="data/manifests")
    ap.add_argument("--train-ratio", type=float, default=0.9)
    ap.add_argument("--dev-ratio", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-prefix", default="corpus")
    args = ap.parse_args()

    entries = load_manifest(args.manifest)
    rnd = random.Random(args.seed)
    rnd.shuffle(entries)

    n = len(entries)
    n_dev = int(n * args.dev_ratio)
    n_test = 0
    if args.train_ratio < 1:
        n_test = int(n * (1 - args.train_ratio))
    dev = entries[:n_dev]
    test = entries[n_dev : n_dev + n_test]
    train = entries[n_dev + n_test :]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, es in (("train", train), ("dev", dev), ("test", test)):
        save_manifest(es, out_dir / f"{args.out_prefix}_{name}.jsonl")
        print(f"{name}: {len(es)}")


if __name__ == "__main__":
    main()
