"""Reproducibility metadata without credentials or environment secrets."""

import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _command(args):
    try:
        return subprocess.check_output(
            args, stderr=subprocess.STDOUT, text=True, timeout=10
        ).strip()
    except Exception as error:
        return "unavailable: {}".format(type(error).__name__)


def git_state(root: Path) -> Dict[str, Any]:
    return {
        "commit": _command(["git", "-C", str(root), "rev-parse", "HEAD"]),
        "branch": _command(["git", "-C", str(root), "branch", "--show-current"]),
        "status_short": _command(["git", "-C", str(root), "status", "--short"]),
        "origin": _command(["git", "-C", str(root), "remote", "get-url", "origin"]),
    }


def environment_text() -> str:
    lines = [
        "timestamp_utc={}".format(datetime.now(timezone.utc).isoformat()),
        "python={}".format(sys.version.replace("\n", " ")),
        "platform={}".format(platform.platform()),
        "hostname={}".format(platform.node()),
        "cpu_count={}".format(os.cpu_count()),
        "nvidia_smi={}".format(_command(["nvidia-smi", "-L"])),
    ]
    for package in ("torch", "transformers", "pandas", "numpy", "pyarrow", "yaml"):
        try:
            module = __import__(package)
            lines.append("{}={}".format(package, getattr(module, "__version__", "unknown")))
        except Exception as error:
            lines.append("{}=unavailable:{}".format(package, type(error).__name__))
    return "\n".join(lines) + "\n"
