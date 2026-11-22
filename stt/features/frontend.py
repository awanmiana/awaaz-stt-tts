"""Log-mel frontend (Phase 0; filled in Phase 2).

80-bin log-mel, 25ms window, 10ms hop by default (matches configs/stt/*.yaml).
"""

from __future__ import annotations

import torch
import torch.nn as nn


class LogMelSpectrogram(nn.Module):
    def __init__(
        self,
        sample_rate: int = 16000,
        n_mels: int = 80,
        win_ms: float = 25.0,
        hop_ms: float = 10.0,
        f_min: float = 0.0,
        f_max: float | None = None,
    ):
        super().__init__()
        self.sample_rate = sample_rate
        self.n_fft = int(sample_rate * win_ms / 1000)
        self.hop = int(sample_rate * hop_ms / 1000)
        self.n_mels = n_mels
        from torchaudio.transforms import MelSpectrogram

        self.mel = MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop,
            n_mels=n_mels,
            f_min=f_min,
            f_max=f_max,
            power=2.0,
            norm="slaney",
            center=True,
        )

    def forward(self, wav: torch.Tensor) -> torch.Tensor:
        """wav: [T] or [B, T] -> log-mel: [T', n_mels] or [B, T', n_mels]."""
        spec = self.mel(wav)
        log_spec = torch.log(spec + 1e-5)
        return log_spec.transpose(-1, -2)


def load_audio(path: str, sample_rate: int = 16000) -> torch.Tensor:
    """Load an audio file to a mono float32 tensor [T] at the given sample rate."""
    import torchaudio
    import torchaudio.functional as F

    wav, sr = torchaudio.load(path)
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0)
    if sr != sample_rate:
        wav = F.resample(wav, sr, sample_rate)
    return wav


if __name__ == "__main__":  # pragma: no cover
    import torch

    m = LogMelSpectrogram()
    out = m(torch.randn(16000))
    print(out.shape)
