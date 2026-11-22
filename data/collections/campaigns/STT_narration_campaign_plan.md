# STT Narration Campaign Plan (Phase 1)

Target: **≥2,000 hrs pure-Urdu STT corpus** (docs/phase1_goals.md; flexible).

Style coverage (roadmap §Style coverage): poetry, debate/argument, academic, street vernacular, everyday, neutral — targets in [COVERAGE_MATRIX.md](COVERAGE_MATRIX.md).

## Model

- Professional narration (studio-grade): voices, accents, clear dictation.
- Read-aloud of prepared utterances + ad-lib coverage (see dev sets in `data/dev/`).
- QC: sample review (5% via `data/scripts/qc_sample.py`); transcript QC (random sample transcription check).

## Sources (mixture; pure Urdu)

- **40% news/journalism:** news articles (5–10 min segments), public-domain Urdu literature, Urdu Wikipedia sentences.
- **25% everyday/conversational:** common phrases, dictation drills, kids' books/stories.
- **15% technical:** engineering/medicine/IT docs, manuals, technical narration.
- **10% poetry/verse:** selected ghazals + Urdu poetry lines (see `data/dev/prompts/poetry.jsonl`).
- **10% debate/argument:** debate segments, commentary (see `data/dev/prompts/debate.jsonl`).

Text normalized via `shared/text_norm.py`; dedup via audio hashes (`data/scripts/audio_qc.py --hash`).

## Coverage matrix (style targets)

| Style | Min hours |
|---|---|
| neutral | 20 |
| everyday | 50 |
| poetry | 40 |
| debate | 40 |
| academic | 40 |
| street vernacular | 40 |

Domain mix: news ≥10h, academic ≥10h, technical ≥5h, medical ≥5h, everyday ≥20h, fiction/poetry ≥10h.

Speakers: ≥3 distinct STT speakers (dev-set balance); recommend 4–6 total.

## Timeline (3–5 months)

- **Week 1–2:** hiring/training; equipment; source prep; agreements with narrators.
- **Month 1:** pilot (50 utts/recorder); style dev sets filled; QC pipeline dry-run (`qc_sample.py`, `audio_qc.py`).
- **Months 2–4:** bulk collection (throughput below); weekly QC passes.
- **Month 4–5:** final QC + storage into `data/raw/<speaker>/`.

## Throughput model

- Target: **~40–60 hrs/month/recorder** (16-bit PCM, 16–24kHz; ~1 hr of audio per minute of recording).
- 2,000 hrs over 3–4 months → 4–6 recorders.
- Recorders: gender-balanced, regional coverage (Lahore/Karachi/Islamabad/etc.).

## Style coverage during recording

- Utterances tagged with `style`/`domain` in metadata CSV (schema: `data/README.md`).
- Recorders read prompts from `data/dev/prompts/*.jsonl` + story excerpts; naturalness for "street" style.

## QC gates (exit criteria, see docs/phase1_goals.md)

1. Volume: ≥2,000 hrs total; per-style minimums met (coverage matrix).
2. Quality: QC sample pass (SNR ≥20dB median, no duplicates, speaker attribution); transcript QC pass.
3. Legal: source licenses approved (see data/collections/README.md).
4. Storage: manifests valid (`python -m data.scripts.make_manifest.py`), raw audio present.

## Exit

Phase 1 exit: data ready for Phase 2 (architecture lock).
