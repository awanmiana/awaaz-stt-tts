# Phase 3 — SSL Pre-training (pure Urdu) (goals & exit gates)

Timeline: **1–3 months (data-dependent)** — pure Urdu audio, success defined by phoneme probe (gate below).

Context: ADR-02b — variant decision: HuBERT by default (Wav2Vec 2.1 alternative; switch if the phoneme probe is poor).

## Deliverables

1. `stt/ssl/` package: `pretrain.py` (entry), `wav2vec2.py` (contrastive skeleton), `hubert.py` (masked units skeleton), `cluster.py` (k-means targets), `dataset.py` (SSL dataset), `eval_phoneme.py` (phoneme-discrimination probe).
2. ADR-02 addendum (variant choice: wav2vec2 vs HuBERT; reasons).
3. Phoneme probe gates + checkpoint saving.

## Timeline

- Week 1: data audit (hours, speakers, format — pure Urdu, no Hindi); variant decision (ADR-02 addendum); masking-ratio tuning plan.
- Weeks 2–8: pretraining on A100s (smoke-test 1 step on CPU first).
- Week 8: phoneme probe eval + checkpoint save.

## Gates (exit)

- Phoneme discrimination probe: per-phoneme recall ≥ 50% on held-out set (baseline for STT fine-tuning; tune on data).
- Checkpoint + training script smoke-tested (1 step, CPU).

## Next

Phase 4 — STT training (FastConformer fine-tune on labeled data) + objectives review.

Campaign plans (execution): [data/collections/campaigns/](../collections/campaigns/).
