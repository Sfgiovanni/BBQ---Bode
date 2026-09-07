"""Checkpointed, resumable scoring runner."""

import gc
import json
import logging
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import numpy as np
import pandas as pd
try:  # adapters served over HTTP need no local tensor stack
    import torch
except ModuleNotFoundError:  # pragma: no cover - exercised only in API-only envs
    torch = None

def _cuda_available() -> bool:
    return torch is not None and torch.cuda.is_available()

def _empty_cache() -> None:
    if _cuda_available():
        torch.cuda.empty_cache()

from brbbq.config import PROJECT_ROOT, dump_config, project_path
from brbbq.dataset import build_dataset, load_catalogs, validate_dataset
from brbbq.models import BaseModelAdapter, create_adapter
from brbbq.scoring.tokens import parse_generated_option
from brbbq.utils.environment import environment_text, git_state
from brbbq.utils.io import atomic_csv, atomic_json, atomic_parquet, run_lock


LOGGER = logging.getLogger("brbbq.run")


def make_run_id(config: Dict[str, Any]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_tag = config["model"]["model_name"].split("/")[-1]
    return "{}_{}_{}".format(timestamp, config["experiment"]["name"], model_tag)


def configure_logging(run_dir: Path) -> None:
    log_path = run_dir / "logs" / "run.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(stream)
    LOGGER.addHandler(file_handler)


def _write_initial_artifacts(config: Dict[str, Any], run_dir: Path) -> pd.DataFrame:
    paths = config["paths"]
    categories_path = project_path(paths["categories"])
    scenarios_path = project_path(paths["scenarios"])
    catalog, scenarios = load_catalogs(categories_path, scenarios_path)
    templates, logical, expanded = build_dataset(categories_path, scenarios_path)
    counts = validate_dataset(catalog, scenarios, templates, logical, expanded)
    dump_config(config, run_dir / "config_resolved.yaml")
    atomic_json(git_state(PROJECT_ROOT), run_dir / "git_state.json")
    (run_dir / "environment.txt").write_text(environment_text(), encoding="utf-8")
    atomic_csv(templates, run_dir / "base_templates.csv")
    atomic_parquet(logical, run_dir / "logical_examples.parquet")
    atomic_parquet(expanded, run_dir / "expanded_examples.parquet")
    dataset_manifest = dict(counts)
    dataset_manifest.update(
        {
            "seed": config["experiment"]["seed"],
            "languages": config["experiment"]["languages"],
            "categories": [category["id"] for category in catalog["categories"]],
            "permutations": 3,
            "unknown_text": catalog["unknown"],
        }
    )
    atomic_json(dataset_manifest, run_dir / "dataset_manifest.json")
    return expanded


def prepare_run(
    config: Dict[str, Any], run_id: Optional[str] = None, resume: bool = False
) -> Tuple[Path, pd.DataFrame]:
    root = project_path(config["paths"]["results_root"])
    root.mkdir(parents=True, exist_ok=True)
    if resume and run_id is None:
        candidates = []
        for manifest_path in root.glob("*/manifest.json"):
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if manifest.get("status") in ("running", "interrupted", "failed"):
                if manifest.get("experiment") == config["experiment"]["name"]:
                    candidates.append(manifest_path.parent)
        if candidates:
            run_dir = sorted(candidates)[-1]
            return run_dir, pd.read_parquet(run_dir / "expanded_examples.parquet")
    resolved_id = run_id or make_run_id(config)
    run_dir = root / resolved_id
    if run_dir.exists() and any(run_dir.iterdir()):
        if (run_dir / "manifest.json").exists():
            status = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8")).get(
                "status"
            )
            if status == "completed":
                raise RuntimeError("A completed run is immutable: {}".format(run_dir))
        if not resume:
            raise RuntimeError("Run directory already exists; use --resume: {}".format(run_dir))
        return run_dir, pd.read_parquet(run_dir / "expanded_examples.parquet")
    for directory in ("checkpoints", "logs", "metrics", "figures"):
        (run_dir / directory).mkdir(parents=True, exist_ok=True)
    expanded = _write_initial_artifacts(config, run_dir)
    manifest = {
        "run_id": resolved_id,
        "experiment": config["experiment"]["name"],
        "status": "initialized",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expected_evaluations": int(len(expanded)),
        "completed_evaluations": 0,
    }
    atomic_json(manifest, run_dir / "manifest.json")
    return run_dir, expanded


def _audit_ids(expanded: pd.DataFrame, per_language: int, seed: int) -> Set[str]:
    selected = []
    rng = np.random.RandomState(seed)
    for language in ("pt", "en"):
        subset = expanded[expanded["language"] == language]
        strata = []
        for _, group in subset.groupby(
            ["category_id", "context_type", "unknown_position"], sort=True
        ):
            strata.append(group.iloc[int(rng.randint(0, len(group)))]["example_id"])
        if len(strata) < per_language:
            remaining = (
                subset[~subset["example_id"].isin(strata)]
                .sample(n=per_language - len(strata), random_state=seed)["example_id"]
                .tolist()
            )
            strata.extend(remaining)
        selected.extend(strata[:per_language])
    return set(selected)


def _probabilities(scores: Dict[str, float]) -> Dict[str, float]:
    values = np.array([scores[letter] for letter in ("A", "B", "C")], dtype=float)
    values = np.exp(values - values.max())
    values = values / values.sum()
    return {letter: float(values[index]) for index, letter in enumerate(("A", "B", "C"))}


def _neutral_baselines(adapter: BaseModelAdapter) -> Dict[str, Any]:
    examples = {
        "pt": {
            "language": "pt",
            "context": "Duas pessoas aguardam, sem outras informações.",
            "question": "Qual alternativa está correta?",
            "option_A": "Primeira alternativa",
            "option_B": "Segunda alternativa",
            "option_C": "Não é possível determinar",
        },
        "en": {
            "language": "en",
            "context": "Two people are waiting, with no other information.",
            "question": "Which option is correct?",
            "option_A": "First option",
            "option_B": "Second option",
            "option_C": "It is not possible to determine",
        },
    }
    prompts = [adapter.render_prompt(examples[language]) for language in ("pt", "en")]
    scored = adapter.score_options(prompts)
    output = {}
    for language, row in zip(("pt", "en"), scored):
        logprobs = {letter: row["logprob_{}".format(letter)] for letter in ("A", "B", "C")}
        output[language] = {
            "logprobs": logprobs,
            "normalized_probabilities": _probabilities(logprobs),
        }
    return output


def _save_progress(
    run_dir: Path, completed: int, total: int, started: float, batch_size: int
) -> None:
    elapsed = max(time.time() - started, 1e-9)
    rate = completed / elapsed
    remaining = total - completed
    progress = {
        "completed": completed,
        "total": total,
        "percent": 100.0 * completed / max(total, 1),
        "elapsed_seconds": elapsed,
        "examples_per_second": rate,
        "eta_seconds": remaining / rate if rate > 0 else None,
        "batch_size": batch_size,
        "last_checkpoint": datetime.now(timezone.utc).isoformat(),
    }
    atomic_json(progress, run_dir / "checkpoints" / "progress.json")


def _is_oom(error: BaseException) -> bool:
    message = str(error).lower()
    if torch is not None and isinstance(error, torch.cuda.OutOfMemoryError):
        return True
    return "out of memory" in message


def run_inference(
    config: Dict[str, Any],
    run_dir: Path,
    expanded: pd.DataFrame,
    adapter: Optional[BaseModelAdapter] = None,
) -> pd.DataFrame:
    """Score all evaluations, atomically checkpointing and resuming by ID."""
    configure_logging(run_dir)
    adapter = adapter or create_adapter(config["model"])
    prediction_path = run_dir / "raw_predictions.parquet"
    if prediction_path.exists():
        prior = pd.read_parquet(prediction_path)
        if prior["example_id"].duplicated().any():
            raise RuntimeError("Checkpoint contains duplicate example_id values")
        rows = prior.to_dict("records")
        done = set(prior["example_id"].astype(str))
    else:
        rows, done = [], set()
    total = len(expanded)
    inference = config["inference"]
    batch_size = inference["batch_size"]
    if batch_size == "auto":
        raise RuntimeError("Run config has batch_size=auto; execute preflight first")
    batch_size = int(batch_size)
    checkpoint_every = int(inference.get("checkpoint_every", 100))
    audit_ids = _audit_ids(
        expanded, int(inference.get("audit_per_language", 50)), int(config["experiment"]["seed"])
    )
    todo = expanded[~expanded["example_id"].astype(str).isin(done)].to_dict("records")
    started = time.time()
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "pid": os.getpid(),
        }
    )
    atomic_json(manifest, manifest_path)

    with run_lock(run_dir / "run.lock"):
        try:
            adapter.load_tokenizer()
            adapter.load_model()
        except KeyboardInterrupt:
            manifest.update(
                {
                    "status": "interrupted",
                    "interruption_reason": "Interrupted during model initialization",
                }
            )
            atomic_json(manifest, manifest_path)
            raise
        except BaseException:
            manifest.update({"status": "failed", "failure_reason": "Model initialization failed"})
            atomic_json(manifest, manifest_path)
            raise
        token_audit_path = run_dir / "metrics" / "option_token_audit.json"
        if token_audit_path.exists() and prediction_path.exists():
            token_audit = json.loads(token_audit_path.read_text(encoding="utf-8"))
        else:
            token_audit = adapter.option_token_metadata()
            token_audit["neutral_baselines"] = _neutral_baselines(adapter)
            atomic_json(token_audit, token_audit_path)
        atomic_json(adapter.metadata(), run_dir / "metrics" / "model_metadata.json")
        LOGGER.info(
            "Starting/resuming %d of %d evaluations with batch=%d", len(todo), total, batch_size
        )
        cursor = 0
        since_save = 0
        try:
            while cursor < len(todo):
                batch = todo[cursor : cursor + batch_size]
                prompts = [adapter.render_prompt(item) for item in batch]
                before = time.time()
                try:
                    scored = adapter.score_options(prompts)
                except RuntimeError as error:
                    if _is_oom(error) and batch_size > 1:
                        batch_size = max(1, batch_size // 2)
                        LOGGER.warning("OOM; reducing batch size to %d and retrying", batch_size)
                        gc.collect()
                        _empty_cache()
                        continue
                    raise
                latency = (time.time() - before) / max(len(batch), 1)
                for example, score, prompt in zip(batch, scored, prompts):
                    row = dict(example)
                    row.update(score)
                    row.update(
                        {
                            "model_name": config["model"]["model_name"],
                            "latency_s": latency,
                            "n_output_tokens": 0,
                            "is_correct": score["predicted_option"] == example["correct_option"],
                            "is_biased_answer": score["predicted_option"]
                            == example["biased_option"],
                            "selected_content": example[
                                "content_of_{}".format(score["predicted_option"])
                            ],
                            "raw_generation": None,
                            "parsed_generation_option": None,
                        }
                    )
                    if example["example_id"] in audit_ids:
                        generated, token_count = adapter.generate_free(
                            prompt, int(inference.get("max_new_tokens_audit", 8))
                        )
                        row["raw_generation"] = generated
                        row["parsed_generation_option"] = parse_generated_option(generated)
                        row["n_output_tokens"] = int(token_count)
                    rows.append(row)
                    done.add(str(example["example_id"]))
                    since_save += 1
                cursor += len(batch)
                if since_save >= checkpoint_every:
                    frame = pd.DataFrame(rows).drop_duplicates("example_id", keep="last")
                    atomic_parquet(frame, prediction_path)
                    _save_progress(run_dir, len(frame), total, started, batch_size)
                    since_save = 0
            result = pd.DataFrame(rows).drop_duplicates("example_id", keep="last")
            if len(result) != total:
                raise RuntimeError(
                    "Observed {} predictions; expected {}".format(len(result), total)
                )
            atomic_parquet(result, prediction_path)
            atomic_csv(result, run_dir / "raw_predictions.csv")
            _save_progress(run_dir, len(result), total, started, batch_size)
            usage = {
                "evaluations": len(result),
                "input_tokens": int(result["n_input_tokens"].sum()),
                "output_tokens": int(result["n_output_tokens"].sum()),
                "mean_input_tokens": float(result["n_input_tokens"].mean()),
                "mean_latency_seconds": float(result["latency_s"].mean()),
                "audit_generations": int(result["raw_generation"].notna().sum()),
            }
            atomic_json(usage, run_dir / "token_usage.json")
            runtime = {
                "duration_seconds": time.time() - started,
                "final_batch_size": batch_size,
                "completed_evaluations": len(result),
                "finished_at": datetime.now(timezone.utc).isoformat(),
            }
            atomic_json(runtime, run_dir / "runtime.json")
            manifest.update({"status": "scored", "completed_evaluations": len(result), **runtime})
            atomic_json(manifest, manifest_path)
            return result
        except KeyboardInterrupt:
            status = "interrupted"
            raise
        except BaseException:
            status = "failed"
            LOGGER.exception("Inference failed")
            raise
        finally:
            if "status" in locals():
                frame = pd.DataFrame(rows).drop_duplicates("example_id", keep="last")
                if len(frame):
                    atomic_parquet(frame, prediction_path)
                _save_progress(run_dir, len(frame), total, started, batch_size)
                manifest.update({"status": status, "completed_evaluations": len(frame)})
                atomic_json(manifest, manifest_path)


def preflight(config: Dict[str, Any], adapter: Optional[BaseModelAdapter] = None) -> Dict[str, Any]:
    """Load, audit tokens, test conservative batches, and estimate duration."""
    # A CPU fallback for this 7B float16 checkpoint is not a useful unattended
    # experiment: it can take days and often hangs during first convolution.
    # Report the hardware block before allocating the model so callers can
    # resume safely after restoring the CUDA driver.
    local_adapter = torch is not None
    if local_adapter and not _cuda_available() and config["model"].get("dtype") in ("float16", "bfloat16"):
        return {
            "scientific_run": False,
            "status": "blocked_hardware",
            "reason": "CUDA is unavailable for the configured half-precision 7B model",
            "cuda_available": False,
            "selected_batch_size": None,
            "estimated_full_seconds": None,
            "estimated_full_hours": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    adapter = adapter or create_adapter(config["model"])
    paths = config["paths"]
    _, _, expanded = build_dataset(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    sample = expanded.groupby(["language", "category_id"], sort=True).head(1).head(18)
    adapter.load_tokenizer()
    adapter.load_model()
    token_metadata = adapter.option_token_metadata()
    prompts = [adapter.render_prompt(row) for row in sample.to_dict("records")]
    candidates = [int(value) for value in config["inference"].get("batch_candidates", [8, 4, 2, 1])]
    tested = []
    selected = None
    per_example = None
    for candidate in candidates:
        batch_prompts = (prompts * (math.ceil(candidate / len(prompts)) + 1))[:candidate]
        before = time.time()
        try:
            adapter.score_options(batch_prompts)
            elapsed = time.time() - before
            tested.append({"batch_size": candidate, "status": "ok", "seconds": elapsed})
            selected = candidate
            per_example = elapsed / candidate
            break
        except RuntimeError as error:
            if not _is_oom(error):
                raise
            tested.append({"batch_size": candidate, "status": "oom"})
            gc.collect()
            _empty_cache()
    if selected is None:
        raise RuntimeError("No batch candidate passed preflight")
    estimate = per_example * int(config["experiment"]["expected_expanded_total"])
    return {
        "scientific_run": False,
        "model": adapter.metadata(),
        "selected_batch_size": selected,
        "tested_batches": tested,
        "seconds_per_example_estimate": per_example,
        "estimated_full_seconds": estimate,
        "estimated_full_hours": estimate / 3600.0,
        "token_audit": token_metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
