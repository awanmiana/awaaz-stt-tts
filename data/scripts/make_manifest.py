"""Build a JSONL manifest from a raw audio directory + optional metadata CSV.

CSV columns (header): audio_path,text,speaker_id,domain,style
  - audio_path: path relative to --root (or absolute)
  - text: Urdu transcript (normalized on save)
  - speaker_id: e.g., spk-01

Phase 0 CLI; filled in Phase 1 with splits + QC filters.
"""

import argparse
import csv
from pathlib import Path

import soundfile as sf

from shared.manifest import ManifestEntry, save_manifest

AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg", ".opus", ".aac", ".m4a", ".pcm", ".aiff"}


def scan_audio(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS)


def load_metadata(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = row.get("audio_path") or row.get("path")
                if key:
                    rows[key.strip()] = row
    return rows


def build_entries(root: Path, metadata: dict[str, dict]) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    for wav in scan_audio(root):
        rel = str(wav.relative_to(root))
        meta = metadata.get(rel) or metadata.get(wav.name) or {}
        duration_s, sample_rate = None, None
        try:
            info = sf.info(str(wav))
            duration_s = float(info.duration)
            sample_rate = info.samplerate
        except Exception:  # noqa: BLE001 - data collection is best-effort
            pass
        entries.append(
            ManifestEntry(
                audio_path=str(wav),
                text=meta.get("text", "") or "",
                speaker_id=meta.get("speaker_id", "unknown"),
                language=meta.get("language", "ur"),
                domain=meta.get("domain") or None,
                style=meta.get("style") or None,
                duration_s=duration_s,
                sample_rate=sample_rate,
                split=meta.get("split", "train"),
            )
        )
    return entries


def main():
    ap = argparse.ArgumentParser(description="Build manifest from raw audio dir.")
    ap.add_argument("--root", required=True, help="Root dir containing raw audio.")
    ap.add_argument("--out", required=True, help="Output manifest jsonl.")
    ap.add_argument("--metadata", default=None, help="Optional metadata CSV.")
    args = ap.parse_args()

    metadata = load_metadata(Path(args.metadata)) if args.metadata else {}
    entries = build_entries(Path(args.root), metadata)
    save_manifest(entries, args.out)
    n_with_text = sum(1 for e in entries if e.text.strip())
    print(f"Manifest: {len(entries)} entries ({n_with_text} with transcripts) -> {args.out}")


if __name__ == "__main__":
    main()
