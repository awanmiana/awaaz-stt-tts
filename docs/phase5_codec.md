# Phase 5 — Codec + Speaker Encoder Training (goals & exit gates)

Starts: after Phase 4 objectives pass (per roadmap).

Timeline: 4–6 weeks.

## Deliverables

1. **Codec training (from scratch):** `tts/train_codec.py` — training loop (recon + GAN losses); checkpoints `artifacts/codec/`.
2. **Speaker encoder training (from scratch):** `tts/train_speaker.py` — margin/contrastive; checkpoints `artifacts/spk_enc/`.
3. **Metrics gates:** codec reconstruction on held-out audio; speaker-sim ≥0.85 on pack voices (`eval/speaker_similarity.py`).

## Timeline

- Week 1: data checks (TTS pack volume vs. `docs/phase1_goals.md`); fill codec trainer.
- Weeks 2–4: codec training (from-scratch RVQ: `tts/codec/*`).
- Weeks 4–5: speaker encoder training.
- Week 6: QC + gates.

## Gates (exit)

- Codec: reconstruction metrics on held-out audio (fill `tts/eval.py` — recon/STOI/MUSHRA-ish).
- Speaker encoder: speaker-sim ≥0.85 on pack voices; enrollment consistency.
- Checkpoints saved.
