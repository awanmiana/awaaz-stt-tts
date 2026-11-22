# Roadmap (final — answers incorporated)

## Objectives matrix (target tier: open-class; stretch: big-five quality)

| Area | Objective | Benchmark / gate |
|---|---|---|
| STT — clean WER | ≤ reference (whisper-large-v3, measured on same pure-Urdu dev set) + margin | per-tier review after Phase 4 |
| STT — style coverage | poetry, debate/argument, academic, street vernacular: clean WER ≤ ref + margin; noisy ≤ ~12% | dev sets per style |
| STT — robustness | worst-10%-speakers ΔWER ≤ +15% | speaker dev slice |
| STT — latency | RTF ≤ 0.3 (A100-class); word timestamps ≤ 200ms | inference gate |
| TTS — quality | UTMOS/MOS ≥ top-open tier (human trials + automated) | gates after Phase 6 |
| TTS — voice similarity | speaker-sim ≥ 0.85 for pack voices; stability across sessions | gates |
| TTS — style | classifier ≥ 85% on style labels; ≥90% human-eval on ≥10 prompts/class | gates |
| TTS — latency | TTFT < 500ms; E2E < 2s (short utterances) | gates |
| Platform | SaaS multi-tenant; OpenAI-compatible REST + streaming; consent + opt-out + disclosure | Phase 7 |

## Size tiers (squeeze-to-perfect)

- Small: <100M params — escalate only if gates miss
- Medium: 100–250M
- Large: 250–500M — better-than-ref if needed

Per-tier gates = objectives above; smallest passing tier wins; report size-vs-quality at program end.

## Phases

| Phase | Window | Exit gate |
|---|---|---|
| 0 Foundation | 2w | repo, libs, tokenizer, data pipeline, tests pass |
| 1 Data collection (flexible volume) | 3–5 mo | STT corpus + TTS voice packs per gates |
| 2 Architecture lock | 2–3w | docs, param budgets, benchmarks plan |
| 3 SSL pre-training (pure Urdu) | 1–3 mo | backbone checkpoint |
| 4 STT training + objectives review | 8–10w | objectives gates (§1) |
| 5 Codec + speaker encoder | 4–6w | codec/encoder metric gates |
| 6 TTS training (style variants) + review | 12–16w | objectives gates (§1) |
| 7 API + SaaS platform | 3–4w | endpoints under SLA |
| 8 Tune, launch, language expansion, revision | ongoing | launch; quarterly objective review |

## Style coverage plan

- STT: poetry, debate/argument, academic, street vernacular (in dev sets — measured objectively).
- TTS: style variants per voice: neutral, warm, energetic, academic, poetic, debate, street vernacular, casual.
