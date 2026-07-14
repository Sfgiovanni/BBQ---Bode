"""Configuration loading and command-line overrides."""

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("Configuration must be a mapping: {}".format(path))
    return value


def project_path(value: str, root: Path = PROJECT_ROOT) -> Path:
    """Resolve a configured path relative to the project root."""
    path = Path(value)
    return path if path.is_absolute() else root / path


def load_config(path: str, root: Path = PROJECT_ROOT) -> Dict[str, Any]:
    """Load an experiment config and its referenced model config."""
    config_path = project_path(path, root)
    config = deepcopy(_load_yaml(config_path))
    model_ref = config.get("model", {}).get("config")
    if not model_ref:
        raise ValueError("Experiment config must define model.config")
    model = _load_yaml(project_path(model_ref, root))
    model.update({k: v for k, v in config.get("model", {}).items() if k != "config"})
    model["config_path"] = str(model_ref)
    config["model"] = model
    config["config_path"] = str(config_path)
    return config


def apply_model_overrides(
    config: Dict[str, Any],
    model_name: Optional[str] = None,
    model_config: Optional[str] = None,
    prompt_style: Optional[str] = None,
    dtype: Optional[str] = None,
    batch_size: Optional[str] = None,
    device_map: Optional[str] = None,
    root: Path = PROJECT_ROOT,
) -> Dict[str, Any]:
    """Return a copied config with explicit CLI values applied."""
    resolved = deepcopy(config)
    if model_config:
        model = _load_yaml(project_path(model_config, root))
        model["config_path"] = model_config
        resolved["model"] = model
    overrides = {
        "model_name": model_name,
        "prompt_style": prompt_style,
        "dtype": dtype,
        "device_map": device_map,
    }
    for key, value in overrides.items():
        if value is not None:
            resolved["model"][key] = value
    if batch_size is not None:
        resolved["inference"]["batch_size"] = (
            batch_size if batch_size == "auto" else int(batch_size)
        )
    return resolved


def dump_config(config: Dict[str, Any], path: Path) -> None:
    """Persist a resolved YAML configuration."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(config, handle, allow_unicode=True, sort_keys=False)
