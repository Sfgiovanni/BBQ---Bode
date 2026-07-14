#!/usr/bin/env python3
"""Single-process preflight + full run to avoid a second 7B model load."""

import argparse
import json
from pathlib import Path

from brbbq.config import load_config
from brbbq.models import create_adapter
from brbbq.reporting import generate_reports
from brbbq.scoring.runner import preflight, prepare_run, run_inference
from brbbq.utils.io import atomic_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiments/bilingual_bode_8h.yaml")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--run-id")
    args = parser.parse_args()
    config = load_config(args.config)
    adapter = create_adapter(config["model"])
    calibration = preflight(config, adapter=adapter)
    if calibration.get("status") == "blocked_hardware" or not calibration.get(
        "selected_batch_size"
    ):
        atomic_json(calibration, Path("results/preflight_20260710_blocked.json"))
        raise SystemExit("Preflight blocked: {}".format(calibration.get("reason", calibration)))
    config["inference"]["batch_size"] = calibration["selected_batch_size"]
    atomic_json(calibration, Path("results/preflight_latest.json"))
    print(
        json.dumps(
            {
                "batch_size": calibration["selected_batch_size"],
                "hours": calibration["estimated_full_hours"],
            }
        )
    )
    run_dir, expanded = prepare_run(config, run_id=args.run_id, resume=args.resume)
    predictions = run_inference(config, run_dir, expanded, adapter=adapter)
    generate_reports(run_dir, config)
    print(json.dumps({"run_dir": str(run_dir), "completed": len(predictions)}))


if __name__ == "__main__":
    main()
