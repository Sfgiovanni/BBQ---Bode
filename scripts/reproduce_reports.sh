#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT/results/runs/20260710_000126_bilingual_bode_bode-7b-alpaca-pt-br-no-peft"
OUTPUT="${1:-$ROOT/reproduced/reference_report}"

fail() {
  echo "Error: $*" >&2
  exit 1
}

command -v python >/dev/null 2>&1 || fail "Python was not found"
[[ -f "$SOURCE/raw_predictions.parquet" ]] || fail "published predictions were not found"
[[ ! -e "$OUTPUT" ]] || fail "output already exists: $OUTPUT (choose another path)"

mkdir -p "$OUTPUT"
cp "$SOURCE/raw_predictions.parquet" "$OUTPUT/"
cp "$SOURCE/config_resolved.yaml" "$OUTPUT/"
cp "$SOURCE/manifest.json" "$OUTPUT/"

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/brbbq-matplotlib}"

python -m brbbq.cli report --run-dir "$OUTPUT"

echo "Reproduced reports and figures: $OUTPUT"
