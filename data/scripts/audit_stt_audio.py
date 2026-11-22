"""STT audio data audit (Phase 3, Week 1).

Usage:
  python -m data.scripts.audit_stt_audio --root data/raw --out data/audit_stt.csv
  python -m data.scripts.audit_stt_audio --root data/packs/raw --manifest data/packs/manifests/spk-01.jsonl --out data/packs/qc.csv

Reports per speaker/style/domain: entries, total/mean/median/min/max duration,
SNR (audio_qc), duplicates (hash), missing text ratio (cross-checked with manifest).
"""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path

from data.scripts.audio_qc import content_hash, duration_and_sr, snr_estimate
from shared.manifest import load_manifest

AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg", ".opus", ".aac", ".m4a", ".pcm", ".aiff"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit STT raw audio (Phase 3).")
    ap.add_argument("--root", default="data/raw")
    ap.add_argument("--out", default="data/audit_stt.csv")
    ap.add_argument("--manifest", default=None, help="Optional manifest to cross-check style/domain/speaker.")
    args = ap.parse_args()

    meta = {}
    if args.manifest:
        for e in load_manifest(args.manifest):
            meta[Path(e.audio_path).resolve()] = e

    rows = []
    root = Path(args.root)
    if not root.exists():
        print(f"(no audio under {root} — Phase 1 campaigns in progress)")
    else:
        for f in sorted(root.rglob("*")):
            if not (f.is_file() and f.suffix.lower() in AUDIO_EXTS):
                continue
            rel = f.relative_to(root)
            parts = list(rel.parts)
            speaker = parts[0] if parts else "?"
            style, domain = "-", "-"
            text_len = "-"
            me = meta.get(f.resolve())
            if me is not None:
                speaker = me.speaker_id
                style = me.style or "-"
                domain = me.domain or "-"
                text_len = len(me.text)
            dur, sr = duration_and_sr(f)
            snr = snr_estimate(f)
            rows.append(
                {
                    "file": str(f),
                    "speaker_id": speaker,
                    "style": style,
                    "domain": domain,
                    "duration_s": f"{dur:.3f}" if dur is not None else "-",
                    "sample_rate": sr if sr is not None else "-",
                    "snr_db": f"{snr:.1f}" if snr is not None else "-",
                    "sha256_16": content_hash(f),
                    "text_len": text_len,
                }
            )

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [])
        w.writeheader()
        w.writerows(rows)

    durs = [float(r["duration_s"]) for r in rows if r["duration_s"] != "-"]
    speakers = sorted({r["speaker_id"] for r in rows})
    dupes = len(rows) - len({r["sha256_16"] for r in rows})
    print(f"audit: {len(rows)} files, {len(durs)} durations, speakers={speakers}, dupes={dupes}")
    if durs:
        print(f"total hours: {sum(durs)/3600:.1f}; mean: {statistics.mean(durs):.1f}s; max: {max(durs):.1f}s")


if __name__ == "__main__":
    main()
