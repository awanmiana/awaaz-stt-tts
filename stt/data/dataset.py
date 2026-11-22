"""STT dataset: audio + normalized text targets (Phase 4).

Text targets: `shared/vocab.py` (STT_VOCAB grapheme IDs). Audio via `stt/features/frontend.py`.
"""

from __future__ import annotations

import torch
from torch.utils.data import Dataset

from shared.manifest import ManifestEntry, load_manifest
from shared.text_norm import normalize_transcript
from shared.vocab import STT_TOKEN_TO_ID
from stt.features.frontend import load_audio


class STTDataset(Dataset):
    def __init__(self, manifest_path: str, sample_rate: int = 16000):
        self.entries: list[ManifestEntry] = load_manifest(manifest_path)
        self.sample_rate = sample_rate

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor | str]:
        e = self.entries[idx]
        text = normalize_transcript(e.text, e.language)
        target_ids = [STT_TOKEN_TO_ID.get(ch, 1) for ch in text]  # 1 = <unk>
        try:
            wav = load_audio(e.audio_path, self.sample_rate)
        except Exception:  # noqa: BLE001 - data-dependent; fill Phase 4
            wav = torch.zeros(800)
        return {
            "waveform": wav,
            "text": text,
            "target_ids": torch.tensor(target_ids, dtype=torch.long),
            "speaker_id": e.speaker_id,
            "style": e.style or "",
        }


def make_batches(dataset: STTDataset, batch_size: int, seed: int = 0, sort_by_duration: bool = True):
    """Simple batching; full bucketing (duration sort) lands in Phase 4 train.py.

    Returns list of index lists.
    """
    import random

    idx = list(range(len(dataset)))
    random.Random(seed).shuffle(idx)
    if sort_by_duration:
        # Rough bucketing: sort by text length (real duration sort in Phase 4).
        idx.sort(key=lambda i: len(dataset[i]["text"]))
    return [idx[i : i + batch_size] for i in range(0, len(idx), batch_size)]


if __name__ == "__main__":  # pragma: no cover
    ds = STTDataset("data/manifests/train.jsonl")
    print(f"STTDataset: {len(ds)} entries; batch_size=8 -> {len(make_batches(ds, 8))} batches")
