# Phase 1 — Data Collection (goals & exit gates)

Timeline: 3–5 months (per roadmap). Exit gate: "data ready for Phase 2 (architecture lock)".

Campaign plans (execution):
- [STT Narration Campaign Plan](../collections/campaigns/STT_narration_campaign_plan.md)
- [TTS Voice Pack Campaign Plan](../collections/campaigns/TTS_voice_pack_campaign_plan.md)

## Targets

### STT corpus (pure Urdu)
- **Total: ≥2,000 hours** (flexible; grows as gates demand — roadmap says "benchmarks decide").
- **Style coverage (from roadmap §Style coverage):** poetry ≥40h, debate ≥40h, academic ≥40h, street ≥40h, everyday ≥50h, neutral ≥20h.
- **Domain mix:** news ≥10h, academic ≥10h, technical ≥5h, medical ≥5h, everyday ≥20h, fiction/poetry ≥10h.
- **Speakers:** ≥3 distinct STT speakers (recommend 4–6 total).
- **Format:** 16–24kHz, 16-bit PCM, normalized (Phase 2/5), deduped, forced-aligned.

### TTS voice packs
- **3 pack voices** (per `configs/tts/default.yaml`: spk-01..spk-03) — more if gates demand.
- Per voice: **≥1.5h audio**; **consent signed** (`data/packs/CONSENT_TEMPLATE.md`); style variants: ≥3 per voice (from `data/packs/VOICES.yaml`).
- **Enrollment data:** short clips (~10–30s) per pack voice for the speaker encoder + cloning path (Phases 5/7).

### Dev sets (benchmark baseline for STT + TTS, per roadmap objectives)
- `data/dev/`: per-style dev sets filled with real recordings of our devs (or approved external reviewers): poetry, debate, academic, street, everyday, neutral — **≥20 utterances per style**.
- Per-style dev WER targets (roadmap: whisper-large-v3 reference + margin) recorded in `docs/benchmarks/stt_table.md` (Phase 4).

## Gates (exit criteria)
1. Volume gates (STT hours per style/domain; TTS pack hours per voice; dev sets filled).
2. Quality gates: sample review pass (QC sample: SNR, duplicates, speaker attribution); transcript QC pass (~5% human transcription check).
3. Legal: public-corpus licenses approved by mid-Phase 1; consent forms for pack voices signed before recording starts.
4. Storage: `data/raw/` + `data/manifests/` populated; manifests valid (run `python -m data.scripts.normalize_transcripts` + `make_manifest` sanity).

## Sources & collection plan

See `data/collections/` (campaigns + public-corpus review list).
