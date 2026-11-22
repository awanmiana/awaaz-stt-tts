"""STT inference entrypoints (filled in Phase 7: OpenAI-compatible API).

Design:
  load_stt_model(ckpt_dir) -> STTModel
  transcribe(wav_path, model) -> str
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch

from stt.decode.beam import greedy_decode_text
from stt.features.frontend import LogMelSpectrogram, load_audio
from stt.model.fastconformer import FastConformerConfig, FastConformerCTC

STTModel = Any


def load_stt_model(ckpt_dir: str | Path) -> STTModel:
    raise NotImplementedError("STT inference wired in Phase 7.")


def transcribe(wav_path: str | Path, model: STTModel) -> str:
    raise NotImplementedError("STT inference wired in Phase 7.")


def _greedy_decode(logits: torch.Tensor) -> str:
    return greedy_decode_text(logits)


if __name__ == "__main__":  # pragma: no cover
    print("STT serve skeleton (Phase 7).")
