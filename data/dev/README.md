# Dev sets (Phase 1)

Per-style dev sets for STT + TTS benchmarking (roadmap objectives).

```
data/dev/
  README.md
  prompts/              # Urdu prompts (reviewers/recorders read these)
    poetry.jsonl
    debate.jsonl
    academic.jsonl
    street.jsonl
    everyday.jsonl
    neutral.jsonl
  dev_poetry.jsonl      # empty skeleton manifests (scaffolded by make_dev_set.py)
  dev_debate.jsonl
  dev_academic.jsonl
  dev_street.jsonl
  dev_everyday.jsonl
  dev_neutral.jsonl
```

- Style set: poetry, debate, academic, street, everyday, neutral.
- Prompt files: Urdu samples per style — reviewed by our devs; read aloud by recorders during Phase 1.
- TTS: same prompts reused for style eval in Phase 6 (`docs/benchmarks/tts_table.md`).
- STT: filled during Phase 1 by recording teams; benchmarked in Phase 4 (roadmap).

Dev-set quality gates: ≥20 utterances per style; ≥3 distinct speakers across styles; style-balanced samples (see `docs/phase1_goals.md`).
