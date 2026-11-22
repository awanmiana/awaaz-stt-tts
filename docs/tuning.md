# Tuning & benchmarks

## Config system

Per-model YAML (`configs/stt/*.yaml`, `configs/tts/*.yaml`). All knobs documented there; overriding per-deployment:

```bash
python -m stt.train --config configs/stt/medium.yaml --override stt.d_model=512
```

## Benchmark workflow (Phase 4/6 fill; setup in Phase 2 — see eval/benchmarks/README.md)

1. **Phase 2**: set up references + dev sets (data/dev/).
2. **After Phase 4 (STT)**: run dev sets through our STT + references; record WER tables in `docs/benchmarks/stt_table.md`; objective review per roadmap.
3. **After Phase 6 (TTS)**: automated (UTMOS/speaker-sim) + human MOS trials; record in `docs/benchmarks/tts_table.md`.
4. **Objective review**: after each phase per the roadmap matrix; adjust targets or model size per the squeeze-to-perfect rule.

Attributes: [docs/attributions.md](attributions.md).

## Knobs (TBD — filled in Phase 2)

- STT: beam_size, lm_weight, beam search + LM fusion; decode chunking; SpecAugment rates; SSL masking ratio.
- TTS: sampling temp/top_p, speed, pitch, style strength, speaker embedding noise scale.

## Optimization (Phase 8+)

Quantization (int8/tensorrt/onnx), distillation (edge models), continuous training, A/B per tenant.
