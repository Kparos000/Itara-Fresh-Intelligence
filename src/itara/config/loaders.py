"""Configuration loading utilities for Itara Fresh Intelligence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file and return a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the YAML file is empty or does not contain a mapping.
    """
    if not path.exists():
        msg = f"Config file does not exist: {path}"
        raise FileNotFoundError(msg)

    with path.open("r", encoding="utf-8") as file:
        loaded = yaml.safe_load(file)

    if loaded is None:
        msg = f"Config file is empty: {path}"
        raise ValueError(msg)

    if not isinstance(loaded, dict):
        msg = f"Config file must contain a YAML mapping: {path}"
        raise ValueError(msg)

    return loaded
