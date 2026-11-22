"""QC sample of a manifest: durations/speakers/styles/missing text (Phase 1).

Usage:
  python -m data.scripts.qc_sample --manifest data/manifests/train.jsonl --n 200 --out data/qc_sample.csv

Writes a CSV sheet for review (durations from soundfile if available).
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from shared.manifest import load_manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="QC sample of a manifest.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", default="data/qc_sample.csv")
    args = ap.parse_args()

    entries = load_manifest(args.manifest)
    rnd = random.Random(0)
    sample = rnd.sample(entries, min(len(entries), args.n)) if entries else []

    sf = None
    try:
        import soundfile as sf  # type: ignore
    except ImportError:
        pass

    rows = []
    for e in sample:
        dur = None
        if sf is not None and e.audio_path and Path(e.audio_path).exists():
            try:
                dur = round(float(sf.info(e.audio_path).duration), 3)
            except Exception:  # noqa: BLE001
                dur = None
        rows.append(
            {
                "audio_path": e.audio_path,
                "speaker_id": e.speaker_id,
                "style": e.style or "-",
                "domain": e.domain or "-",
                "text_len": len(e.text),
                "missing_text": 0 if e.text else 1,
                "duration_s": f"{dur}" if dur is not None else "-",
                "sample_rate": e.sample_rate or "-",
            }
        )

    fieldnames = list(rows[0].keys()) if rows else []
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    total_dur = sum(r["duration_s"] and float(r["duration_s"]) or 0 for r in rows)
    print(f"QC sample: {len(rows)} rows -> {args.out}; total sampled duration: {total_dur:.0f}s")


if __name__ == "__main__":
    main()
