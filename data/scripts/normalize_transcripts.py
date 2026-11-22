"""Normalize transcripts in a manifest (in-place or --out).

Phase 0 CLI. Phase 1: batch-mode batch normalization for large corpora.
"""

import argparse

from shared.manifest import load_manifest, save_manifest
from shared.text_norm import normalize_transcript


def normalize_entries(entries):
    for e in entries:
        e.text = normalize_transcript(e.text, e.language)
    return entries


def main():
    ap = argparse.ArgumentParser(description="Normalize transcripts in a manifest.")
    ap.add_argument("--manifest", required=True, help="Input manifest jsonl.")
    ap.add_argument("--out", default=None, help="Output manifest (default: in-place).")
    args = ap.parse_args()

    entries = normalize_entries(load_manifest(args.manifest))
    out = args.out or args.manifest
    save_manifest(entries, out)
    print(f"Normalized {len(entries)} entries -> {out}")


if __name__ == "__main__":
    main()
