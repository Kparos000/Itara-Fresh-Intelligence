import csv
import json
from pathlib import Path
from typing import Any

from itara.geo import generate_network_artifacts


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_generate_network_artifacts_writes_expected_files(tmp_path: Path) -> None:
    paths = generate_network_artifacts(tmp_path)

    assert paths.network_nodes_path.exists()
    assert paths.distance_matrix_path.exists()
    assert paths.network_summary_path.exists()


def test_generated_network_nodes_artifact_has_expected_shape(tmp_path: Path) -> None:
    paths = generate_network_artifacts(tmp_path)

    nodes = _load_json(paths.network_nodes_path)

    assert len(nodes) == 26
    assert nodes[0]["node_type"] == "warehouse"
    assert {"node_id", "node_type", "node_name", "coordinates", "metadata"}.issubset(
        nodes[0].keys()
    )


def test_generated_distance_matrix_artifact_has_expected_shape(tmp_path: Path) -> None:
    paths = generate_network_artifacts(tmp_path)

    with paths.distance_matrix_path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 26 * 25
    assert rows[0]["origin_node_id"]
    assert rows[0]["destination_node_id"]
    assert float(rows[0]["straight_line_distance_km"]) >= 0.0


def test_generated_network_summary_artifact_has_expected_counts(tmp_path: Path) -> None:
    paths = generate_network_artifacts(tmp_path)

    summary = _load_json(paths.network_summary_path)

    assert summary["total_nodes"] == 26
    assert summary["node_type_counts"] == {
        "store": 15,
        "supplier": 10,
        "warehouse": 1,
    }
    assert summary["distance_matrix_entries"] == 650
    assert summary["max_estimated_road_distance_km"] > 0
    assert summary["max_estimated_drive_minutes"] > 0
