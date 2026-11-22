"""STT evaluation on dev manifests (Phase 4 target; skeleton now).

Outputs: WER/CER table by style/domain/speaker.
"""

from __future__ import annotations

import argparse

import torch

from eval.wer import cer, wer
from shared.config_util import load_config
from shared.manifest import load_manifest
from shared.text_norm import normalize_transcript
from stt.decode.beam import greedy_decode_text
from stt.features.frontend import LogMelSpectrogram, load_audio
from stt.model.fastconformer import FastConformerConfig, FastConformerCTC


def evaluate(model, entries, frontend, decode_fn) -> list[dict]:
    rows = []
    for e in entries:
        try:
            wav = load_audio(e.audio_path, model_sample_rate())
            feats = frontend(wav)
            logits = model(feats.unsqueeze(0))
            pred = decode_fn(logits[0])
        except Exception:  # noqa: BLE001
            pred = ""
        rows.append(
            {
                "style": e.style or "-",
                "domain": e.domain or "-",
                "speaker": e.speaker_id,
                "wer": wer(e.text, pred),
                "cer": cer(e.text, pred),
                "ref_len": len(normalize_transcript(e.text, "ur").split()),
            }
        )
    return rows


def model_sample_rate() -> int:
    return 16000


def print_table(rows):
    if not rows:
        print("(no entries)")
        return
    header = ["style", "domain", "speaker", "wer", "cer", "ref_len"]
    print(" | ".join(header))
    print("-" * 60)
    for r in rows:
        print(" | ".join(str(r[h]) for h in header))


def main():
    ap = argparse.ArgumentParser(description="Evaluate STT model on dev manifests.")
    ap.add_argument("--config", default="configs/stt/small.yaml")
    ap.add_argument("--model", default="artifacts/stt/stt-v0.1-small.pth")
    ap.add_argument("--manifest", default="data/manifests/dev.jsonl")
    args = ap.parse_args()

    cfg = load_config(args.config)
    entries = load_manifest(args.manifest)
    frontend = LogMelSpectrogram(
        sample_rate=cfg["stt"]["sample_rate"], n_mels=cfg["stt"]["n_mels"]
    )
    try:
        ckpt = torch.load(args.model, map_location="cpu")
        stt_cfg = FastConformerConfig(
            d_model=cfg["stt"]["d_model"],
            n_layers=cfg["stt"]["n_layers"],
            n_heads=cfg["stt"]["n_heads"],
        )
        model = FastConformerCTC(stt_cfg, vocab_size=cfg["stt"]["vocab_size"])
        model.load_state_dict(ckpt)
        model.eval()
    except FileNotFoundError:
        print(f"[eval] checkpoint not found: {args.model} — metrics run after Phase 2/4 training.")
        rows = []
        print_table(rows)
        return

    rows = evaluate(model, entries, frontend, greedy_decode_text)
    overall = sum(r["wer"] for r in rows) / max(len(rows), 1)
    print(f"\nOverall WER: {overall:.3f}")
    print_table(rows)


if __name__ == "__main__":
    main()
