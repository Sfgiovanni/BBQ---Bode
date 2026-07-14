#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="${1:-}"
if [[ -z "$RUN_DIR" ]]; then RUN_DIR="$(find "$ROOT/results/runs" -mindepth 1 -maxdepth 1 -type d | sort | tail -1)"; fi
echo "run_dir=$RUN_DIR"
if [[ -f "$RUN_DIR/checkpoints/progress.json" ]]; then cat "$RUN_DIR/checkpoints/progress.json"; else echo "progress=not_started"; fi
echo "-- GPU --"; nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "GPU unavailable"
echo "-- lock --"; [[ -f "$RUN_DIR/run.lock" ]] && cat "$RUN_DIR/run.lock" || echo "not locked"
echo "-- log tail --"; tail -n 20 "$RUN_DIR/logs/run.log" 2>/dev/null || true
