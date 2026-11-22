# Style & Domain Coverage Matrix (Phase 1 targets)

From docs/phase1_goals.md + roadmap §Style coverage.

## STT style coverage (per style: min hours + dev prompts)

| Style | Min hours (STT) | Dev prompts |
|---|---|---|
| poetry | 40 | data/dev/prompts/poetry.jsonl |
| debate | 40 | data/dev/prompts/debate.jsonl |
| academic | 40 | data/dev/prompts/academic.jsonl |
| street vernacular | 40 | data/dev/prompts/street.jsonl |
| everyday | 50 | data/dev/prompts/everyday.jsonl |
| neutral | 20 | data/dev/prompts/neutral.jsonl |

## STT domain mix

| Domain | Min hours |
|---|---|
| news | 10 |
| academic | 10 |
| technical | 5 |
| medical | 5 |
| everyday/fiction | 20–30 |

## Speakers

- ≥3 distinct STT speakers for dev-set balance; recommend 4–6 total.

## TTS style variants per voice (VOICES.yaml)

From `data/packs/VOICES.yaml` — e.g., spk-01: [warm, neutral, energetic, academic]; spk-02: [neutral, academic, poetic, debate]; spk-03: [warm, energetic, street, casual].

## TTS dev prompts

- Same Urdu prompts in `data/dev/prompts/*.jsonl` reused for TTS style eval in Phase 6 (`docs/benchmarks/tts_table.md`).
