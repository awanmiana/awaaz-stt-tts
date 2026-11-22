# Phase 4 — Start Gate (data)

STT training starts when Phase 3 weekly audits pass (see
`data/collections/campaigns/phase3_weekly_audit_plan.md` and `docs/phase3_ssl.md`):

- Audit pass 1: volume ≥10% of targets; SNR median ≥20dB; duplicates = 0; speakers ≥1.

When the gate passes:

1. **STT training:** `python -m stt.train --config configs/stt/small.yaml` (real loop — Phase 4 fills `stt/train.py`: bucketing, CTC loss, AdamW + cosine decay, FSDP2/DDP).
2. **SSL fine-tune:** reuse Phase 3 checkpoint (artifacts/ssl) + STT head.
3. **Benchmarks:** run vs. whisper-large-v3 + big-five refs on dev sets (`docs/benchmarks/stt_table.md`); objectives review (`docs/phase4_stt.md`).

Gate check: `python -m data.scripts.coverage_summary --audit data/audit_stt.csv --out data/coverage_weekly.csv`.
