"""Style/domain/speaker coverage summary from audit CSV (Phase 3, weekly).

Usage:
  python -m data.scripts.coverage_summary --audit data/audit_stt.csv --out data/coverage_weekly.csv
  python -m data.scripts.coverage_summary --audit data/audit_stt.csv --matrix data/collections/campaigns/COVERAGE_MATRIX.md --out data/coverage_weekly.csv
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

DEFAULT_MATRIX = "data/collections/campaigns/COVERAGE_MATRIX.md"
DEFAULT_SPEAKERS = 3


def _parse_matrix(path: Path):
    text = path.read_text(encoding="utf-8")
    style_targets: dict[str, int] = {}
    domain_targets: dict[str, int] = {}
    speaker_target = DEFAULT_SPEAKERS
    section = None
    for line in text.splitlines():
        if line.startswith("## STT style coverage"):
            section = "style"
            continue
        if line.startswith("## STT domain mix"):
            section = "domain"
            continue
        if line.startswith("## Speakers"):
            section = "speakers"
            continue
        if section == "speakers":
            mm = re.search(r"(\d+)\s+distinct STT speakers", line)
            if mm:
                speaker_target = int(mm.group(1))
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or not cells[0]:
                continue
            if cells[0].startswith(("Style", "Domain")):
                continue
            m = re.search(r"\d+", cells[1])
            if not m:
                continue
            hours = int(m.group(0))
            key = cells[0].lower()
            if section == "style":
                style_targets[key.replace("street vernacular", "street")] = hours
            elif section == "domain":
                domain_targets[key] = hours
    return style_targets, domain_targets, speaker_target


def main() -> None:
    ap = argparse.ArgumentParser(description="Coverage summary from audit CSV (Phase 3, weekly).")
    ap.add_argument("--audit", required=True)
    ap.add_argument("--matrix", default=DEFAULT_MATRIX)
    ap.add_argument("--out", default="data/coverage_weekly.csv")
    args = ap.parse_args()

    styles, domains, spk_target = _parse_matrix(Path(args.matrix))

    agg_style: dict[str, float] = {}
    agg_domain: dict[str, float] = {}
    speakers: set[str] = set()
    try:
        with open(args.audit, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                try:
                    dur = float(r["duration_s"])
                except (TypeError, ValueError):
                    continue
                style = (r.get("style") or "-").strip()
                agg_style[style] = agg_style.get(style, 0.0) + dur / 3600.0
                domain = (r.get("domain") or "-").strip()
                agg_domain[domain] = agg_domain.get(domain, 0.0) + dur / 3600.0
                spk = (r.get("speaker_id") or "").strip()
                if spk and spk != "-":
                    speakers.add(spk)
    except FileNotFoundError:
        print(f"(no audit file: {args.audit} — run data/scripts/audit_stt_audio.py first)")

    def status(hours: float, target: float) -> str:
        return "OK" if hours >= target else f"SHORT ({hours:.1f}/{target})"

    rows = []
    for s, tgt in styles.items():
        h = agg_style.get(s, 0.0)
        rows.append({"metric": f"style:{s}", "hours": f"{h:.1f}", "target": str(tgt), "status": status(h, tgt)})
    for d, tgt in domains.items():
        h = agg_domain.get(d, 0.0)
        rows.append({"metric": f"domain:{d}", "hours": f"{h:.1f}", "target": str(tgt), "status": status(h, tgt)})
    rows.append(
        {
            "metric": "speakers",
            "hours": f"{len(speakers)}",
            "target": str(spk_target),
            "status": status(float(len(speakers)), float(spk_target)),
        }
    )

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "hours", "target", "status"])
        w.writeheader()
        w.writerows(rows)

    print(f"coverage summary -> {args.out}: {len(rows)} metrics")
    for r in rows:
        print(f"{r['metric']:24s} hours={r['hours']:>6s} target={r['target']:>3s} {r['status']}")


if __name__ == "__main__":
    main()
