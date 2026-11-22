"""SSL dataset: raw waveforms from manifest (Phase 0; SSL use starts Phase 3).

SSL training is unsupervised: uses audio only (transcripts unused for masking,
but preserved in manifest for downstream STT Phase 4).
"""

from __future__ import annotations

import torch
from torch.utils.data import Dataset

from shared.manifest import ManifestEntry, load_manifest
from stt.features.frontend import load_audio


class SSLManifestDataset(Dataset):
    def __init__(self, manifest_path: str, sample_rate: int = 16000):
        self.entries: list[ManifestEntry] = load_manifest(manifest_path)
        self.sample_rate = sample_rate

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor | str]:
        e = self.entries[idx]
        try:
            wav = load_audio(e.audio_path, self.sample_rate)
        except Exception:  # noqa: BLE001 - SSL data-dependent; fill Phase 3
            wav = torch.zeros(100)
        return {"waveform": wav, "speaker_id": e.speaker_id, "style": e.style or ""}


if __name__ == "__main__":  # pragma: no cover
    print("SSLManifestDataset skeleton (Phase 3).")
