# train/ — launchers (Phase 2/4/6)

# Run STT training (all visible GPUs; torchrun):
#   bash train/run_stt.sh --config configs/stt/small.yaml
# run_stt.sh:
#   torchrun --standalone --nproc_per_node=$(python -c "import torch;print(torch.cuda.device_count() or 1)") \
#     stt/train.py --config <cfg> [--manifest data/manifests/train.jsonl] [--resume ...]

# Run codec training (Phase 5):
#   bash train/run_codec.sh

# Run TTS LM training (Phase 6):
#   bash train/run_tts.sh --config configs/tts/default.yaml
