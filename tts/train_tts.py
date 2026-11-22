"""Codec-LM training entry (Phase 0 skeleton; filled in Phase 6)."""

from __future__ import annotations

import argparse

import torch

from shared.config_util import load_config
from tts.model.codec_lm import CodecLM


def main():
    ap = argparse.ArgumentParser(description="Train Codec-LM (skeleton; Phase 6).")
    ap.add_argument("--config", default="configs/tts/default.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)["tts"]
    model = CodecLM(**cfg["acoustic"])
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[Phase 0] Codec-LM skeleton train entry (params: {n_params/1e6:.1f}M). Real training starts Phase 6.")
    print(f"config: {cfg['acoustic']}")

    # Skeleton CE training loop (filled Phase 6):
    # for batch (text_ids, speaker_emb, style_emb, speech_tokens):
    #   logits = model(text_ids, speaker_emb, style_emb);
    #   loss = CE(logits, speech_tokens); + CFG on style (optional); backward.


if __name__ == "__main__":
    main()
