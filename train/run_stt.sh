#!/usr/bin/env bash
# Run STT training (skeleton; filled in Phase 2/4)
set -euo pipefail

CFG="${1:-configs/stt/small.yaml}"
NPROC="$(python -c "import torch; print(torch.cuda.device_count() or 1)")"

torchrun --standalone --nproc_per_node="$NPROC" stt/train.py --config "$CFG" "${@:2}"
