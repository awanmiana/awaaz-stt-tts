"""Codec training entry (Phase 5).

Usage: python tts/train_codec.py --config configs/tts/default.yaml

Skeleton now (Phase 0); Phase 5 fills:
- data: TTS pack manifests (data/packs/manifests/*.jsonl) -> mel batches
- losses: recon (z vs z_hat) + codec decoder recon (mel vs dec(z_hat)) + GAN (optional)
- checkpoints: artifacts/codec/
"""

from __future__ import annotations

import argparse

import torch

from shared.config_util import load_config
from tts.codec.decoder import ConvDecoder
from tts.codec.encoder import ConvEncoder
from tts.codec.quantizer import ResidualVectorQuantizer


def build_models(cfg: dict):
    codec = cfg["tts"]["codec"]
    enc = ConvEncoder(latent_dim=codec["latent_dim"])
    vq = ResidualVectorQuantizer(
        latent_dim=codec["latent_dim"], n_codebooks=codec["codebooks"], codebook_size=codec["codebook_size"]
    )
    dec = ConvDecoder(latent_dim=codec["latent_dim"])
    return enc, vq, dec


def codec_losses(enc, vq, dec, mel: torch.Tensor) -> dict[str, torch.Tensor]:
    z = enc(mel)  # [B, D, T]
    ids = vq.encode(z)  # [B, K, T]
    z_hat = vq.decode(ids)  # [B, D, T]
    recon = torch.nn.functional.mse_loss(mel, dec(z_hat))
    vq_losses = vq.losses(z, z_hat)
    return {"recon": recon, **vq_losses}


def main() -> None:
    ap = argparse.ArgumentParser(description="Codec training entry (Phase 5 fill).")
    ap.add_argument("--config", default="configs/tts/default.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)["tts"]

    enc, vq, dec = build_models(cfg)
    opt = torch.optim.AdamW(list(enc.parameters()) + list(vq.parameters()) + list(dec.parameters()))

    print("[Phase 5] Codec trainer skeleton — real training loop starts Phase 5.")
    n_params = sum(p.numel() for p in enc.parameters() + vq.parameters() + dec.parameters())
    print(f"params: {n_params/1e6:.1f}M")

    # Real loop (Phase 5): pack manifests -> mel batches -> codec_losses -> backward.
    # skeleton: batch = {"mel": [B, T, F]}; losses = codec_losses(...); opt.step().


if __name__ == "__main__":
    main()
