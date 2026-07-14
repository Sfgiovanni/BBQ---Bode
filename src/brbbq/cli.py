"""Command-line entry points for validation, inference, and reporting."""

import argparse
import json
from pathlib import Path


from brbbq.config import apply_model_overrides, load_config, project_path
from brbbq.dataset import build_dataset, load_catalogs, validate_dataset
from brbbq.reporting import generate_reports
from brbbq.scoring.runner import preflight, prepare_run, run_inference
from brbbq.utils.io import atomic_json, atomic_parquet, atomic_csv


def _config(args):
    config = load_config(args.config)
    return apply_model_overrides(
        config,
        model_name=getattr(args, "model_name", None),
        model_config=getattr(args, "model_config", None),
        prompt_style=getattr(args, "prompt_style", None),
        dtype=getattr(args, "dtype", None),
        batch_size=getattr(args, "batch_size", None),
        device_map=getattr(args, "device_map", None),
    )


def command_validate(args):
    config = _config(args)
    paths = config["paths"]
    catalog, scenarios = load_catalogs(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    templates, logical, expanded = build_dataset(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    counts = validate_dataset(catalog, scenarios, templates, logical, expanded)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    return 0


def command_build(args):
    config = _config(args)
    paths = config["paths"]
    catalog, scenarios = load_catalogs(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    templates, logical, expanded = build_dataset(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    counts = validate_dataset(catalog, scenarios, templates, logical, expanded)
    output = Path(args.output) if args.output else project_path("results/dataset_build")
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(templates, output / "base_templates.csv")
    atomic_parquet(logical, output / "logical_examples.parquet")
    atomic_parquet(expanded, output / "expanded_examples.parquet")
    atomic_json(counts, output / "dataset_manifest.json")
    print(json.dumps({"output": str(output), **counts}, ensure_ascii=False, indent=2))
    return 0


def command_preflight(args):
    config = _config(args)
    result = preflight(config)
    if args.output:
        atomic_json(result, Path(args.output))
    config["inference"]["batch_size"] = result["selected_batch_size"]
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print("selected_batch_size={}".format(result["selected_batch_size"]))
    return 0 if result.get("status", "ok") == "ok" or result.get("selected_batch_size") else 2


def command_run(args):
    config = _config(args)
    if config["inference"].get("batch_size") == "auto":
        result = preflight(config)
        if result.get("status") == "blocked_hardware" or not result.get("selected_batch_size"):
            raise RuntimeError(
                "Preflight blocked the scientific run: {}".format(result.get("reason", result))
            )
        config["inference"]["batch_size"] = result["selected_batch_size"]
        preflight_path = project_path(config["paths"]["results_root"]) / "PRELIGHT_{}.json".format(
            config["experiment"]["name"]
        )
        atomic_json(result, preflight_path)
        print(
            "Preflight selected batch_size={} (estimated {:.2f} hours)".format(
                result["selected_batch_size"], result["estimated_full_hours"]
            )
        )
    run_dir, expanded = prepare_run(config, run_id=args.run_id, resume=args.resume)
    print("run_dir={}".format(run_dir))
    predictions = run_inference(config, run_dir, expanded)
    generate_reports(run_dir, config, with_bootstrap=not args.no_bootstrap)
    print("completed={} run_dir={}".format(len(predictions), run_dir))
    return 0


def command_report(args):
    run_dir = Path(args.run_dir)
    config_path = run_dir / "config_resolved.yaml"
    if config_path.exists():
        import yaml

        with config_path.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
    else:
        config = load_config(args.config)
    generate_reports(run_dir, config, with_bootstrap=not args.no_bootstrap)
    print("reports={}".format(run_dir))
    return 0


def _parser():
    parser = argparse.ArgumentParser(prog="brbbq")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(command):
        command.add_argument("--config", default="configs/experiments/bilingual_bode_8h.yaml")
        command.add_argument("--model-name")
        command.add_argument("--model-config")
        command.add_argument("--prompt-style")
        command.add_argument("--dtype")
        command.add_argument("--batch-size")
        command.add_argument("--device-map")

    validate = sub.add_parser("validate")
    common(validate)
    validate.set_defaults(function=command_validate)
    build = sub.add_parser("build-dataset")
    common(build)
    build.add_argument("--output")
    build.set_defaults(function=command_build)
    pf = sub.add_parser("preflight")
    common(pf)
    pf.add_argument("--output")
    pf.set_defaults(function=command_preflight)
    run = sub.add_parser("run")
    common(run)
    run.add_argument("--resume", action="store_true")
    run.add_argument("--run-id")
    run.add_argument("--no-bootstrap", action="store_true")
    run.set_defaults(function=command_run)
    report = sub.add_parser("report")
    report.add_argument("--run-dir", required=True)
    report.add_argument("--config", default="configs/experiments/bilingual_bode_8h.yaml")
    report.add_argument("--no-bootstrap", action="store_true")
    report.set_defaults(function=command_report)
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    return args.function(args)


if __name__ == "__main__":
    raise SystemExit(main())
