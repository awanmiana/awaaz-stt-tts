"""Manifest schema + I/O (Phase 0).

A manifest is a JSONL file; each line is a `ManifestEntry` as a dict.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator

from shared.text_norm import normalize_transcript

# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


@dataclass
class ManifestEntry:
    audio_path: str
    text: str
    speaker_id: str
    language: str = "ur"
    domain: str | None = None
    duration_s: float | None = None
    sample_rate: int | None = None
    style: str | None = None
    split: str = "train"
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.text = normalize_transcript(self.text, self.language)
        if self.duration_s is not None:
            self.duration_s = float(self.duration_s)

    @property
    def text_norm(self) -> str:
        return normalize_transcript(self.text, self.language)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ManifestEntry":
        return cls(
            audio_path=d["audio_path"],
            text=d["text"],
            speaker_id=d["speaker_id"],
            language=d.get("language", "ur"),
            domain=d.get("domain"),
            duration_s=d.get("duration_s"),
            sample_rate=d.get("sample_rate"),
            style=d.get("style"),
            split=d.get("split", "train"),
            extra=d.get("extra", {}),
        )

    def __repr__(self) -> str:  # pragma: no cover
        return f"ManifestEntry({self.audio_path!r}, spk={self.speaker_id!r}, split={self.split})"


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------


def save_manifest(entries: list[ManifestEntry], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")


def load_manifest(path: str | Path) -> list[ManifestEntry]:
    path = Path(path)
    entries: list[ManifestEntry] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(ManifestEntry.from_dict(json.loads(line)))
    return entries


def iter_manifest(path: str | Path) -> Iterator[ManifestEntry]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield ManifestEntry.from_dict(json.loads(line))


def filter_split(entries: list[ManifestEntry], split: str) -> list[ManifestEntry]:
    return [e for e in entries if e.split == split]


def group_by_speaker(entries: list[ManifestEntry]) -> dict[str, list[ManifestEntry]]:
    out: dict[str, list[ManifestEntry]] = {}
    for e in entries:
        out.setdefault(e.speaker_id, []).append(e)
    return out


if __name__ == "__main__":  # pragma: no cover
    e = ManifestEntry(audio_path="data/x.wav", text="ہیلو", speaker_id="spk-01")
    print(e.to_dict())
