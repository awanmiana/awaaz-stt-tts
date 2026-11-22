#!/usr/bin/env bash
# Run TTS training: codec (Phase 5) or Codec-LM (Phase 6)
set -euo pipefail

WHAT="${1:-tts}"
shift || true

case "$WHAT" in
  codec)
    python tts/train_codec.py --config configs/tts/default.yaml "$@"
    ;;
  tts|codec-lm)
    python tts/train_tts.py --config configs/tts/default.yaml "$@"
    ;;
  *)
    echo "usage: $0 [codec|tts] [args...]" >&2
    exit 1
    ;;
esac
