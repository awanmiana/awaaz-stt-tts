"""Speaker encoder training entry (Phase 5).

Skeleton (Phase 0); Phase 5 fills:
- data: TTS pack audio (data/packs/raw/*) -> mel batches
- loss: margin/contrastive over speaker IDs (triplet or AAM-style; from scratch)
- checkpoints: artifacts/spk_enc/
"""

from __future__ import annotations

import argparse

import torch

from shared.config_util import load_config
from tts.speaker_encoder import SpeakerEncoder


def triplet_margin_loss(anchor: torch.Tensor, positive: torch.Tensor, negative: torch.Tensor, margin: float = 0.25) -> torch.Tensor:
    """Margin loss on speaker embeddings (sim to positive minus sim to negative)."""
    sim_pos = (anchor * positive).sum(dim=-1)
    sim_neg = (anchor * negative).sum(dim=-1)
    return torch.clamp(margin - sim_pos + sim_neg, min=0).mean()


def main() -> None:
    ap = argparse.ArgumentParser(description="Speaker encoder training entry (Phase 5 fill).")
    ap.add_argument("--config", default="configs/tts/default.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)["tts"]

    enc = SpeakerEncoder(emb_dim=cfg["speaker_encoder"]["emb_dim"])
    opt = torch.optim.AdamW(enc.parameters(), lr=1e-3)

    print("[Phase 5] Speaker encoder trainer skeleton — real loop starts Phase 5.")
    print(f"emb_dim: {cfg['speaker_encoder']['emb_dim']}")

    # Real loop (Phase 5): pack audio -> mel -> anchor/positive/negative batches
    # -> triplet_margin_loss / AAM-style loss -> backward.


if __name__ == "__main__":
    main()
