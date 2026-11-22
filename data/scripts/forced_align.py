"""Forced alignment helpers (Phase 5 — MFA toolchain).

Pipeline (planned in Phase 5):
1. Collect: text (normalized) + audio per utterance.
2. Align: Montreal Forced Aligner (MFA) — `mfa align` (English model for Urdu? use
   MFA's Urdu-compatible aligner or train one), produce TextGrid intervals.
3. Export: intervals -> manifest `duration_s` / segment info.

Stub: probe durations; align_segment documented; full wrapper filled in Phase 5.
"""

import argparse
import json
from pathlib import Path
from typing import Any


def probe_duration(audio_path: str) -> float | None:
    try:
        import soundfile as sf

        return float(sf.info(audio_path).duration)
    except Exception:  # noqa: BLE001
        return None


def align_command(textgrid_out: str, audio_dir: str, out_json: str) -> dict[str, Any]:
    """Export MFA textgrid intervals to a JSON segments file (interface only)."""
    segments: list[dict[str, Any]] = []
    for tg in Path(textgrid_out).rglob("*.TextGrid"):
        segments.append({"textgrid": str(tg), "file": str(tg.with_suffix(""))})
    out = Path(out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"n_files": len(segments), "out": str(out)}


def main():
    ap = argparse.ArgumentParser(description="Forced-alignment helpers (stub; MFA).")
    ap.add_argument("--textgrid-out", required=True)
    ap.add_argument("--audio-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = align_command(args.textgrid_out, args.audio_dir, args.out)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
