"""Path utilities for the Itara Fresh Intelligence repository."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the repository root based on this source file location."""
    return Path(__file__).resolve().parents[3]


def data_dir() -> Path:
    """Return the data directory."""
    return repo_root() / "data"


def config_dir() -> Path:
    """Return the static configuration directory."""
    return data_dir() / "config"


def generated_data_dir() -> Path:
    """Return the generated data directory."""
    return data_dir() / "generated"


def docs_dir() -> Path:
    """Return the docs directory."""
    return repo_root() / "docs"
