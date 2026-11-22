# Phase 3 — Data Audit (STT, pure Urdu) (Week 1)

Audit data/raw (collected during Phase 1 campaigns; audit begins when data arrives, then weekly).

```
python -m data.scripts.audit_stt_audio --root data/raw --out data/audit_stt.csv
python -m data.scripts.audit_stt_audio --root data/packs/raw --manifest data/packs/manifests/spk-01.jsonl --out data/packs/qc.csv
```

Deliverables:
- Volume: total hours; hours per style/domain/speaker (vs. docs/phase1_goals.md gates).
- Quality: SNR distribution (≥20dB median target, per `data/scripts/audio_qc.py`), duplicates (hash), missing-text ratio.
- Coverage: speaker balance (goal: ≥3 STT speakers; recommend 4–6).

Variant decision (ADR-02 addendum):
- Decision: HuBERT (default). Switch to Wav2Vec 2.1 if phoneme probe is poor (gate: per-phoneme recall ≥50%, docs/phase3_ssl.md).

Data-dependent adjustments:
- If hours < target: extend Phase 1 campaigns; adapt masking ratios (configs/stt/ssl_*.yaml).
- Train on collected data once audits pass.
