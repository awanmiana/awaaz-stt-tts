# Phase 4 — STT Training + Objectives Review (goals & exit gates)

Starts when: Phase 3 audit pass 1 OK — or as data flows. Exit: benchmarks meet roadmap objectives (docs/benchmarks/stt_table.md).

Timeline: 8–10 weeks (per roadmap).

## Deliverables

1. **Dataset/dataloader (filled):** `stt/data/dataset.py` — audio + normalized text targets (grapheme IDs, shared/vocab.py), bucketing.
2. **Training loop (filled):** `stt/train.py` — CTC loss (or RNN-T), AdamW + cosine decay, SpecAugment, FSDP2/DDP, logging (MLflow), checkpoints (artifacts/stt/).
3. **SSL-pretrained fine-tune:** reuse SSL encoder (Phase 3) + STT head (ADR-02b variant).
4. **Decoding (filled):** `stt/decode/beam.py` — beam search + KenLM fusion (from-scratch KenLM trained on Urdu text); timestamps.
5. **Objectives review:** run benchmarks vs. whisper-large-v3 + big-five refs on dev sets (docs/benchmarks/stt_table.md); per roadmap objectives (docs/roadmap.md §Objectives matrix); adjust targets/size per squeeze-to-perfect.

## Timeline

- Week 1: data checks (audit pass 1); dataset/dataloader (bucketing) — `stt/data/dataset.py`.
- Weeks 2–7: STT training; mid-run eval (dev WER).
- Week 8: WER eval on dev sets + objective review (docs/benchmarks/stt_table.md) + checkpoint save.

## Gates (exit)

- Audit pass 1 OK (Phase 3).
- WER per style/domain vs. roadmap objectives (docs/benchmarks/stt_table.md):
  - Small tier: WER ≤ whisper-large-v3 + margin (see roadmap objectives).
- Model saved (artifacts/stt/<tier>.pth).

## Next: Phase 5 — Codec training (Phase 5, per roadmap).
