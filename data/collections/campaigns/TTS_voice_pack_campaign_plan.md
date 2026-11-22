# TTS Voice Pack Campaign Plan (Phase 1)

3 pack voices (`spk-01`..`spk-03` — see `data/packs/VOICES.yaml`) + enrollment path (Phases 5/7).

## Voices

- `spk-01` (female, Lahore) — style variants: warm, neutral, energetic, academic
- `spk-02` (male, Karachi) — style variants: neutral, academic, poetic, debate
- `spk-03` (female, Islamabad) — style variants: warm, energetic, street, casual

## Throughput

- Per voice: **≥1.5h studio audio**; ~6–8 prompts/min → ~50 prompts/hr → ~90 min total per voice (2–3 sessions).
- Total: ~4.5h voice-pack audio + enrollment clips (10–30s each; ~20 per voice = ~10 min).
- Studio, quiet room; 24kHz, 16-bit PCM.

## Prompts

- Read-aloud: `data/dev/prompts/*.jsonl` (style sets) + story excerpts.
- Multiple takes per prompt (2–3); naturalness over perfection (esp. for "street").

## Consent & legal

- Sign `data/packs/CONSENT_TEMPLATE.md` per voice (opt-in, opt-out, disclosure) **before** recording.
- Register speakers in `data/packs/speakers_registry.csv`.

## Enrollment data (Phases 5/7)

- 10–30s clips per pack voice (from the recording session) for the speaker encoder + cloning path.

## Timeline

- Weeks 1–2: contracts + registry + prompt prep.
- Weeks 3–10: pack recording (3 voices in parallel; 2–3 sessions each).
- Weeks 10–13: QC + manifests + style eval prompts (`data/packs/style_prompts/<voice-id>/<style>.jsonl`).

## Exit

3 voices with ≥1.5h each (docs/phase1_goals.md); manifests valid via `python -m data.scripts.make_manifest`.
