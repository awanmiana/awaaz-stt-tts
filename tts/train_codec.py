"""Codec training entry (Phase 0 skeleton; filled in Phase 5)."""

from __future__ import annotations

import argparse

import torch

from shared.config_util import load_config
from tts.codec.decoder import ConvDecoder
from tts.codec.encoder import ConvEncoder
from tts.codec.quantizer import ResidualVectorQuantizer


def main():
    ap = argparse.ArgumentParser(description="Train TTS codec (skeleton; Phase 5).")
    ap.add_argument("--config", default="configs/tts/default.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)["tts"]
    enc = ConvEncoder(latent_dim=cfg["codec"]["latent_dim"])
    dec = ConvDecoder(latent_dim=cfg["codec"]["latent_dim"])
    vq = ResidualVectorQuantizer(
        latent_dim=cfg["codec"]["latent_dim"],
        n_codebooks=cfg["codec"]["codebooks"],
        codebook_size=cfg["codec"]["codebook_size"],
    )
    opt = torch.optim.AdamW(list(enc.parameters()) + list(vq.parameters()) + list(dec.parameters()))

    # Skeleton training loop (filled in Phase 5):
    # for mel_batch in data: z = enc(mel); ids = vq.encode(z); z_hat = vq.decode(ids);
    # losses = vq.losses(z, z_hat) + recon(wav, dec(z_hat)) + GAN loss (optional); backward.
    print("[Phase 0] Codec skeleton train entry. Real training starts Phase 5.")
    print(f"config: codec={cfg['codec']}")
    n_params = sum(p.numel() for p in enc.parameters() + vq.parameters() + dec.parameters())
    print(f"params: {n_params/1e6:.1f}M")


if __name__ == "__main__":
    main()
