# Tuning & benchmarks

## Config system

Per-model YAML (`configs/stt/*.yaml`, `configs/tts/*.yaml`). All knobs documented there; overriding per-deployment:

```bash
python -m stt.train --config configs/stt/medium.yaml --override stt.d_model=512
```

## Benchmark workflow

1. **Phase 2**: set up references (see `eval/benchmarks/README.md`).
2. **After Phase 4 (STT)**: run dev sets through our STT + references; record WER tables in `docs/benchmarks/stt.md`.
3. **After Phase 6 (TTS)**: human MOS/UEMOS trials + automated UTMOS/speaker-sim; record in `docs/benchmarks/tts.md`.
4. **Objective review**: after each phase per the roadmap matrix; adjust targets or model size per the squeeze-to-perfect rule.

## Knobs (TBD — filled in Phase 0/2)

- STT: beam_size, lm_weight, beam search + LM fusion; decode chunking; SpecAugment rates; SSL masking ratio.
- TTS: sampling temp/top_p, speed, pitch, style strength, speaker embedding noise scale.

## Optimization (Phase 8+)

Quantization (int8/tensorrt/onnx), distillation (edge models), continuous training, A/B per tenant.
