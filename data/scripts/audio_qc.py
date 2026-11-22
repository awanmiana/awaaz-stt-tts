"""Audio QC helpers (Phase 1): duration, RMS/SNR estimate, content hash.

Usage:
  python -m data.scripts.audio_qc --dir data/packs/raw/spk-01 --out data/packs/qc_spk-01.csv
  python -m data.scripts.audio_qc --hash --dir data/packs/raw --out data/packs/hashes.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from pathlib import Path

AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg", ".opus", ".aac", ".m4a", ".pcm", ".aiff"}


def iter_audio(dir_path: Path):
    return sorted(p for p in dir_path.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS)


def duration_and_sr(path: Path) -> tuple[float | None, int | None]:
    try:
        import soundfile as sf

        info = sf.info(str(path))
        return float(info.duration), int(info.samplerate)
    except Exception:  # noqa: BLE001
        return None, None


def snr_estimate(path: Path) -> float | None:
    """RMS-based SNR estimate: signal = 95th percentile of 5ms RMS frames,
    noise = min frame RMS (approximation; fine for QC gating)."""
    try:
        import numpy as np
        import soundfile as sf

        data, sr = sf.read(str(path), dtype="float32", always_2d=False)
        if data.ndim > 1:
            data = data.mean(axis=1)
        data = data.astype(np.float32)
        if data.size == 0 or sr <= 0:
            return None
        frame = max(1, int(sr * 0.005))
        n = (len(data) // frame) * frame
        frames = data[:n].reshape(-1, frame)
        rms_frames = np.sqrt(np.mean(frames ** 2, axis=1) + 1e-10)
        if rms_frames.size == 0:
            return None
        signal = float(np.percentile(rms_frames, 95))
        noise = float(np.min(rms_frames))
        if signal <= 0 or noise <= 0:
            return None
        return 20.0 * math.log10(signal / noise)
    except Exception:  # noqa: BLE001
        return None


def content_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def main() -> None:
    ap = argparse.ArgumentParser(description="Audio QC: duration/SNR/hashes (Phase 1).")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--hash", action="store_true", help="Include content hashes (duplicate detection).")
    args = ap.parse_args()

    rows = []
    for f in iter_audio(Path(args.dir)):
        dur, sr = duration_and_sr(f)
        snr = snr_estimate(f)
        row = {
            "file": str(f),
            "duration_s": f"{dur:.3f}" if dur is not None else "-",
            "sample_rate": sr if sr is not None else "-",
            "snr_db": f"{snr:.1f}" if snr is not None else "-",
        }
        if args.hash:
            row["sha256_16"] = content_hash(f)
        rows.append(row)

    out = args.out
    if out:
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
            w.writeheader()
            w.writerows(rows)
        print(f"audio QC: {len(rows)} files -> {out}")
    else:
        for r in rows:
            print(r)


if __name__ == "__main__":
    main()
