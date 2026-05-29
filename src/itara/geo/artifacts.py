"""Generate reusable network artifacts for the simulator and map visualizer."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from itara.config import load_stores, load_suppliers, load_warehouse
from itara.domain import DistanceMatrixEntry, MapNode
from itara.geo.distance import build_directed_distance_matrix, build_network_nodes
from itara.utils import generated_data_dir


@dataclass(frozen=True)
class NetworkArtifactPaths:
    """Paths written by the network artifact generator."""

    network_nodes_path: Path
    distance_matrix_path: Path
    network_summary_path: Path


def _write_json(path: Path, payload: Any) -> None:
    """Write a JSON artifact."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)


def _write_distance_matrix_csv(
    path: Path,
    distance_matrix: tuple[DistanceMatrixEntry, ...],
) -> None:
    """Write the directed distance matrix as CSV."""
    fieldnames = [
        "origin_node_id",
        "destination_node_id",
        "straight_line_distance_km",
        "estimated_road_distance_km",
        "estimated_drive_minutes",
    ]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in distance_matrix:
            writer.writerow(entry.model_dump(mode="json"))


def _build_network_summary(
    nodes: tuple[MapNode, ...],
    distance_matrix: tuple[DistanceMatrixEntry, ...],
) -> dict[str, Any]:
    """Build a compact summary of the generated network."""
    node_type_counts = Counter(node.node_type.value for node in nodes)
    road_distances = [
        entry.estimated_road_distance_km
        for entry in distance_matrix
        if entry.estimated_road_distance_km is not None
    ]
    drive_minutes = [
        entry.estimated_drive_minutes
        for entry in distance_matrix
        if entry.estimated_drive_minutes is not None
    ]

    return {
        "total_nodes": len(nodes),
        "node_type_counts": dict(sorted(node_type_counts.items())),
        "distance_matrix_entries": len(distance_matrix),
        "max_estimated_road_distance_km": max(road_distances, default=0.0),
        "max_estimated_drive_minutes": max(drive_minutes, default=0.0),
    }


def generate_network_artifacts(output_dir: Path | None = None) -> NetworkArtifactPaths:
    """Generate network nodes, distance matrix, and network summary artifacts."""
    target_dir = output_dir or generated_data_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()

    nodes = build_network_nodes(stores, warehouse, suppliers)
    distance_matrix = build_directed_distance_matrix(nodes)

    network_nodes_path = target_dir / "network_nodes.json"
    distance_matrix_path = target_dir / "distance_matrix.csv"
    network_summary_path = target_dir / "network_summary.json"

    _write_json(
        network_nodes_path,
        [node.model_dump(mode="json") for node in nodes],
    )
    _write_distance_matrix_csv(distance_matrix_path, distance_matrix)
    _write_json(
        network_summary_path,
        _build_network_summary(nodes, distance_matrix),
    )

    return NetworkArtifactPaths(
        network_nodes_path=network_nodes_path,
        distance_matrix_path=distance_matrix_path,
        network_summary_path=network_summary_path,
    )


def main() -> None:
    """Generate network artifacts from the command line."""
    paths = generate_network_artifacts()
    print(f"Wrote {paths.network_nodes_path}")
    print(f"Wrote {paths.distance_matrix_path}")
    print(f"Wrote {paths.network_summary_path}")
