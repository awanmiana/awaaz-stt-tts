# Benchmarks (Phase 4–6 fill; setup in Phase 2)

## STT benchmark setup (run after Phase 4 training)

Per-style dev sets: `data/dev/dev_<style>.jsonl` (poetry, debate, academic, street, everyday, neutral).

### Objective tiers (roadmap objectives; measured on our pure-Urdu dev sets)

| Tier | Objective |
|---|---|
| Small (<100M) | whisper-large-v3 WER + margin (reference tier — see below) |
| Medium (100–250M) | whisper-large-v3 WER (baseline) |
| Large (250–500M) | whisper-large-v3 WER − margin |

Reference runs (benchmarks against the big-five + whisper-large-v3):

| Reference | How | Access notes |
|---|---|---|
| whisper-large-v3 | `pip install transformers`; transcribe dev sets | Urdu-supported; open |
| Google Gemini Live | Google AI API (Gemini Live models); transcribe dev sets | Requires Google account/API key; check Urdu support |
| OpenAI Whisper API (ChatGPT tier) | `openai` package; `whisper-1`; transcribe dev sets | Requires API key; Urdu support varies |
| Microsoft Azure Speech (STT) | Azure Speech-to-Text; transcribe dev sets | Requires Azure subscription |
| Meta SeamlessM4T v2 | `seamless_m4t_v2_large` via transformers/hub | Open model (Hugging Face hub) |

Deliverables: `docs/benchmarks/stt_table.md` — WER by style/domain/speaker per tier vs. references; pass criteria from roadmap.

## TTS benchmark setup (run after Phase 6 training)

Automated:
- **UTMOS** (public UTMOS model as automated proxy) — per tier.
- **Speaker similarity:** our speaker encoder on enrollments vs. outputs (target ≥0.85).
- **Style accuracy:** our StyleClassifier (target ≥85%); human eval ≥90% on ≥10 prompts/class (see below).

Human: MOS via listening trials on ≥10 prompts/style/tier (`docs/benchmarks/tts_table.md`).

Prompts: same Urdu prompts as `data/dev/prompts/*.jsonl` (style-balanced; reused from STT dev sets).

Reference tiers (from roadmap objectives): top-open TTS (CosyVoice-2/NaturalSpeech-3-class; note in tables that these are reference tiers, measured via automated metrics where accessible, otherwise by design review).

## Notes

- Proprietary products: no published per-language benchmarks — measure ourselves on dev sets; note access limitations.
- GitHub: weights on HF Hub (`huggingface.co/awaniana/awaaz-stt-tts`).
