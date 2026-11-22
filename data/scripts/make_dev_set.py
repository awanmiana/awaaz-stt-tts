"""Scaffold empty dev manifests from prompts (Phase 1).

Usage:
  python -m data.scripts.make_dev_set --prompts-dir data/dev/prompts --out-dir data/dev
                                       [--styles poetry debate ...] [--n 12]

Writes `data/dev/dev_<style>.jsonl` skeletons (audio_path empty — filled by recordings in Phase 1).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from shared.manifest import ManifestEntry, save_manifest


def scaffold(prompt_path: Path, out_path: Path, n: int) -> None:
    entries: list[ManifestEntry] = []
    if prompt_path.exists():
        with open(prompt_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                entries.append(
                    ManifestEntry(
                        audio_path="",  # PENDING — filled by Phase 1 recordings
                        text=rec["prompt"],
                        speaker_id="spk-dev",
                        language="ur",
                        domain=rec.get("domain") or "dev",
                        style=rec["style"],
                        split="dev",
                    )
                )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_manifest(entries[:n], out_path)
    print(f"{out_path}: {len(entries[:n])} entries (audio pending)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold empty dev manifests from prompts.")
    ap.add_argument("--prompts-dir", default="data/dev/prompts")
    ap.add_argument("--out-dir", default="data/dev")
    ap.add_argument("--styles", nargs="+", default=["poetry", "debate", "academic", "street", "everyday", "neutral"])
    ap.add_argument("--n", type=int, default=12)
    args = ap.parse_args()

    for s in args.styles:
        scaffold(Path(args.prompts_dir) / f"{s}.jsonl", Path(args.out_dir) / f"dev_{s}.jsonl", args.n)


if __name__ == "__main__":
    main()
