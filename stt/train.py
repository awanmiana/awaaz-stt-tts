"""STT training entry (Phase 0 skeleton; filled in Phase 2/4).

Run:
  torchrun --standalone --nproc_per_node=<N> stt/train.py --config configs/stt/small.yaml
"""

from __future__ import annotations

import argparse
import time

import torch

from shared.config_util import load_config
from shared.manifest import load_manifest
from stt.features.frontend import LogMelSpectrogram
from stt.model.fastconformer import FastConformerConfig, FastConformerCTC
from stt.model.rnnt import RNNTModel


def build_model(cfg: dict) -> torch.nn.Module:
    stt_cfg = FastConformerConfig(
        d_model=cfg["stt"]["d_model"],
        n_layers=cfg["stt"]["n_layers"],
        n_heads=cfg["stt"]["n_heads"],
    )
    model = FastConformerCTC(stt_cfg, vocab_size=cfg["stt"]["vocab_size"])
    return model.to(cfg["device"])


def load_dataset(manifest_path: str):
    return load_manifest(manifest_path)  # [ManifestEntry, ...]


def train_loop(model, dataset, cfg, *, max_steps: int = 1):
    """Skeleton: standard supervised loop; batches/bucketing in Phase 2."""
    opt = torch.optim.AdamW(model.parameters(), lr=cfg["stt"]["lr"])
    start = time.time()
    for step in range(1, max_steps + 1):
        opt.zero_grad()
        # placeholder batch
        feats = torch.randn(4, 100, 80)
        logits = model(feats)
        loss = logits.mean()  # real loss in Phase 2 (CTC/RNNT)
        loss.backward()
        opt.step()
        if step % 10 == 0:
            print(f"[step {step}/{max_steps}] loss={loss.item():.4f} t={time.time()-start:.0f}s")
    return model


def main():
    ap = argparse.ArgumentParser(description="Train STT model (skeleton; filled Phase 2/4).")
    ap.add_argument("--config", required=True, help="YAML config (configs/stt/*.yaml).")
    ap.add_argument("--manifest", default="data/manifests/train.jsonl")
    ap.add_argument("--dev-manifest", default="data/manifests/dev.jsonl")
    ap.add_argument("--resume", default=None)
    args = ap.parse_args()

    cfg = load_config(args.config)
    cfg["device"] = "cuda" if torch.cuda.is_available() else "cpu"

    model = build_model(cfg)
    dataset = load_dataset(args.manifest)
    print(f"[Phase 0] Skeleton run. Entries={len(dataset)} (real training starts Phase 2.)")
    train_loop(model, dataset, cfg, max_steps=cfg["stt"]["max_steps"])


if __name__ == "__main__":
    main()
