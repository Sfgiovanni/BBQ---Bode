#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p results/runs/logs
LOCK="results/runs/bilingual_bode.launch.lock"
if ( set -o noclobber; echo "$$" > "$LOCK" ) 2>/dev/null; then
  trap 'rm -f "$LOCK"' EXIT
else
  echo "Another bilingual launch is active: $LOCK" >&2; exit 1
fi
LOG="results/runs/launcher_$(date +%Y%m%d_%H%M%S).log"
echo "PID=$$ LOG=$LOG"
exec > >(tee -a "$LOG") 2>&1
ARGS=(--config configs/experiments/bilingual_bode_8h.yaml --resume)
if [[ -f results/preflight_latest.json ]] && python -c 'import json,sys; d=json.load(open("results/preflight_latest.json")); sys.exit(0 if d.get("selected_batch_size") else 1)'; then
  BATCH="$(python -c 'import json; print(json.load(open("results/preflight_latest.json"))["selected_batch_size"])')"
  ARGS+=(--batch-size "$BATCH")
  echo "Using preflight batch size $BATCH"
fi
python -m brbbq.cli run "${ARGS[@]}"
