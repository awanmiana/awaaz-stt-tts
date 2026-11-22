"""STT training entry (Phase 4 fills the real loop).

Usage:
  torchrun --standalone --nproc_per_node=<N> stt/train.py --config configs/stt/small.yaml

Phase 4: real loop — dataset, batches, CTC loss, optimizer (AdamW + cosine),
SpecAugment, FSDP2/DDP, logging (MLflow), checkpoints (artifacts/stt/).
"""

from __future__ import annotations

import argparse
import time

import torch

from shared.config_util import load_config
from stt.data.dataset import STTDataset, make_batches
from stt.features.frontend import LogMelSpectrogram
from stt.model.fastconformer import FastConformerConfig, FastConformerCTC


def build_model(cfg: dict) -> torch.nn.Module:
    stt_cfg = FastConformerConfig(
        d_model=cfg["stt"]["d_model"],
        n_layers=cfg["stt"]["n_layers"],
        n_heads=cfg["stt"]["n_heads"],
    )
    return FastConformerCTC(stt_cfg, vocab_size=cfg["stt"]["vocab_size"])


def compute_loss(model, batch, frontend, device):
    """CTC loss over normalized grapheme targets (RNN-T variant in Phase 4)."""
    wave = batch["waveform"].to(device)
    feats = frontend(wave)  # [B, T', F]
    logits = model(feats)  # [B, T', V]
    log_probs = torch.log_softmax(logits, dim=-1).transpose(0, 1)  # [T', B, V]
    loss_fn = torch.nn.CTCLoss(blank=0, reduction="mean", zero_infinity=True)
    targets = torch.nn.utils.rnn.pad_sequence([item["target_ids"] for item in batch], batch_first=True).to(device)
    input_lengths = torch.full((targets.shape[0],), logits.shape[1], dtype=torch.long).to(device)
    target_lengths = torch.tensor([item["target_ids"].shape[0] for item in batch], dtype=torch.long).to(device)
    return loss_fn(log_probs, targets, input_lengths, target_lengths)


def train_loop(model, dataset, frontend, cfg, dev_dataset=None) -> None:
    opt = torch.optim.AdamW(model.parameters(), lr=cfg["stt"]["lr"], weight_decay=0.01)
    batches = make_batches(dataset, cfg["stt"]["batch_size"])
    steps = 0
    start = time.time()
    for epoch in range(cfg["stt"].get("max_epochs", 1)):
        for batch in batches:
            opt.zero_grad()
            loss = compute_loss(model, batch, frontend, cfg["device"])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            steps += 1
            if steps % 50 == 0:
                print(f"[step {steps}/epoch{epoch}] loss={loss.item():.4f} t={time.time()-start:.0f}s")
    print(f"Done: {steps} steps in {time.time()-start:.0f}s (real loop starts Phase 4).")


def main() -> None:
    ap = argparse.ArgumentParser(description="Train STT model (Phase 4 fills real loop).")
    ap.add_argument("--config", required=True, help="YAML config (configs/stt/*.yaml).")
    ap.add_argument("--manifest", default="data/manifests/train.jsonl")
    ap.add_argument("--dev-manifest", default="data/manifests/dev.jsonl")
    ap.add_argument("--resume", default=None)
    args = ap.parse_args()

    cfg = load_config(args.config)
    cfg["device"] = "cuda" if torch.cuda.is_available() else "cpu"

    frontend = LogMelSpectrogram(sample_rate=cfg["stt"]["sample_rate"], n_mels=cfg["stt"]["n_mels"])
    dataset = STTDataset(args.manifest, cfg["stt"]["sample_rate"])
    model = build_model(cfg)
    train_loop(model, dataset, frontend, cfg)


if __name__ == "__main__":
    main()
