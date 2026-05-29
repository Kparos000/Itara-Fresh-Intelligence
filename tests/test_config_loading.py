from pathlib import Path

import pytest

from itara.config import load_yaml_file
from itara.utils import config_dir, data_dir, docs_dir, generated_data_dir, repo_root


def test_repo_paths_exist() -> None:
    root = repo_root()

    assert root.exists()
    assert data_dir() == root / "data"
    assert config_dir() == root / "data" / "config"
    assert generated_data_dir() == root / "data" / "generated"
    assert docs_dir() == root / "docs"


def test_load_yaml_file_reads_mapping(tmp_path: Path) -> None:
    config_path = tmp_path / "example.yaml"
    config_path.write_text("name: Itara\ncount: 3\n", encoding="utf-8")

    loaded = load_yaml_file(config_path)

    assert loaded == {"name": "Itara", "count": 3}


def test_load_yaml_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_yaml_file(tmp_path / "missing.yaml")


def test_load_yaml_file_rejects_empty_file(tmp_path: Path) -> None:
    config_path = tmp_path / "empty.yaml"
    config_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_yaml_file(config_path)


def test_load_yaml_file_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "list.yaml"
    config_path.write_text("- one\n- two\n", encoding="utf-8")

    with pytest.raises(ValueError, match="mapping"):
        load_yaml_file(config_path)
