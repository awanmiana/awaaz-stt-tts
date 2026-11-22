# Phase 3 — Weekly Audit Plan (execution now; Phase 1 campaigns run in parallel)

Audit runs weekly:

```
python -m data.scripts.audit_stt_audio --root data/raw --out data/audit_stt.csv
python -m data.scripts.coverage_summary --audit data/audit_stt.csv --out data/coverage_weekly.csv
```

Schedule:
- First run after each style set completes (poetry, debate, academic, street, everyday, neutral) — see `data/dev/` and campaigns.
- Weekly thereafter: coverage summary vs. `docs/phase1_goals.md` + `campaigns/COVERAGE_MATRIX.md`.

Checkpoints (campaigns/README.md milestones, adapted for audit):
- M1 (Month 1): audit pass 1 — volume ≥10% of targets; SNR median ≥20dB; no duplicates; speakers ≥1.
- M2 (Month 2–3): audit pass 2 — volume ≥50%; style coverage balance.
- M3 (Month 3–5): audit pass 3 — targets met (`docs/phase1_goals.md`); move to Phase 4.

Actions when SHORT (`coverage_weekly.csv`):
- Volume: extend Phase 1 campaigns (recorders; extra time).
- Quality: SNR — re-record outliers (use `data/audit_stt.csv`); duplicates — remove (hash, `data/scripts/audio_qc.py --hash`).
- Balance: add speakers/styles.

Gate: "audit pass" = all `status: OK` in coverage summary vs. `docs/phase1_goals.md`.

Note: pretraining starts when volume ≥ target and quality passes (`docs/phase3_ssl.md`).
