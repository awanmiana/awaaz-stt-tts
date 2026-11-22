# Phase 2 — Architecture Lock (goals & exit gates)

Timeline: 2–3 weeks. Exit gate: "architecture locked for Phases 3–6" (per roadmap).

Campaign plans (execution): [data/collections/campaigns/](../collections/campaigns/).

## Deliverables

1. **STT locked:** encoder + decoder choice (ADR-01/02 below), param budgets per tier (configs/stt/*.yaml reviewed), SpecAugment/bucketing/seed plan.
2. **TTS locked:** acoustic model choice (ADR-03 — codec-LM default), codec design (ADR-04), speaker + style design (ADR-05).
3. **Benchmarks setup** (docs/benchmarks/*, eval/benchmarks/README.md): reference-run plan vs. whisper-large-v3 + big-five products; dev-set usage plan per style.
4. **Data-path plan:** tokenization (STT graphemes via `shared/vocab.py`; TTS phonemes via G2P), bucketing/padding, prosody priors (Phase 5).
5. **Sizing plan:** param budget per tier vs. Phase 1 data (docs/phase1_goals.md): small-tier gate — WER within roadmap margin of whisper-large-v3 target.

## Timeline

- Week 1: ADR review + writing (docs/architecture_decisions.md, updated architecture.md).
- Week 2: locked configs validated (CPU smoke tests: FastConformer forward, CodecLM forward, codec encoder/decoder shapes); benchmark plan written.

## Gates (exit)

- Architecture documents approved: [docs/architecture_decisions.md](../architecture_decisions.md), [docs/architecture.md](../architecture.md).
- All config files valid; smoke tests pass (`python -m stt.model.fastconformer`? — run inline tests).
- Benchmark procedure documented and ready for Phase 4 (STT) / Phase 6 (TTS).
