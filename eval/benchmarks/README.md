# eval/benchmarks — benchmark setup & harness docs (Phase 4/6 targets)

# Benchmark plan (filled in Phases 4–6):

## STT (after Phase 4)

Reference runs (on pure-Urdu dev sets per style, per roadmap):

1. **Our STT** (this repo, any tier): decode dev set, compute WER/CER per style/domain.
2. **whisper-large-v3** (open): same dev set → open-class tier baseline.
3. **Google Gemini Live** (if accessible): same audio → transcribe.
4. **OpenAI Whisper API** (ChatGPT tier, if accessible): same audio.
5. **Microsoft Azure Speech** (STT): same audio.
6. **Meta SeamlessM4T v2**: same audio.

Deliverables: `docs/benchmarks/stt_table.md` with WER columns; pass criteria from roadmap.

## TTS (after Phase 6)

Automated:
- UTMOS (per-deployment, e.g., via a public UTMOS model — used as an automated proxy).
- Speaker similarity: extract speaker embeddings with our speaker encoder on enrollments vs. outputs.
- Speed/pitch control verification (stable over repeated runs).

Human:
- MOS via listening trials on ≥10 prompts/style/tier.

Deliverables: `docs/benchmarks/tts_table.md`.

## Setup notes

- whisper-large-v3: `pip install transformers && transformers-cli` —Urdu-supported.
- OpenAI Whisper API: needs API key; model `whisper-1`.
- Google Gemini Live / Azure Speech / Meta SeamlessM4T v2: require accounts/keys; measure during dev.
- Proprietary tiers: no published per-language numbers — we measure on dev sets; note any access limitations in the table.
