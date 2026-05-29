import pytest

from itara.config import load_stores, load_suppliers, load_warehouse
from itara.domain import NetworkNodeType
from itara.geo import (
    build_directed_distance_matrix,
    build_network_nodes,
    calculate_haversine_distance_km,
    estimate_drive_minutes,
    estimate_road_distance_km,
)


def test_haversine_distance_between_store_and_warehouse_is_positive() -> None:
    stores = load_stores()
    warehouse = load_warehouse()

    distance_km = calculate_haversine_distance_km(
        stores[0].coordinates,
        warehouse.coordinates,
    )

    assert distance_km > 0
    assert distance_km < 50


def test_road_distance_estimate_is_not_less_than_straight_line_distance() -> None:
    straight_line_distance_km = 10.0

    road_distance_km = estimate_road_distance_km(straight_line_distance_km)

    assert road_distance_km >= straight_line_distance_km


def test_road_distance_rejects_invalid_multiplier() -> None:
    with pytest.raises(ValueError, match="multiplier"):
        estimate_road_distance_km(10.0, multiplier=0.9)


def test_drive_minutes_rejects_invalid_speed() -> None:
    with pytest.raises(ValueError, match="average_speed"):
        estimate_drive_minutes(10.0, average_speed_kmph=0)


def test_build_network_nodes_creates_expected_node_counts() -> None:
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()

    nodes = build_network_nodes(stores, warehouse, suppliers)

    assert len(nodes) == 26

    node_types = [node.node_type for node in nodes]
    assert node_types.count(NetworkNodeType.WAREHOUSE) == 1
    assert node_types.count(NetworkNodeType.STORE) == 15
    assert node_types.count(NetworkNodeType.SUPPLIER) == 10


def test_build_network_nodes_includes_map_metadata() -> None:
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()

    nodes = build_network_nodes(stores, warehouse, suppliers)
    king_west_node = next(node for node in nodes if node.node_id == "store_001")

    assert king_west_node.node_type == NetworkNodeType.STORE
    assert king_west_node.region == "Old Toronto"
    assert king_west_node.metadata["store_format"] == "large_urban"


def test_directed_distance_matrix_has_expected_size() -> None:
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()
    nodes = build_network_nodes(stores, warehouse, suppliers)

    distance_matrix = build_directed_distance_matrix(nodes)

    assert len(distance_matrix) == len(nodes) * (len(nodes) - 1)


def test_directed_distance_matrix_excludes_self_distances() -> None:
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()
    nodes = build_network_nodes(stores, warehouse, suppliers)

    distance_matrix = build_directed_distance_matrix(nodes)

    assert all(entry.origin_node_id != entry.destination_node_id for entry in distance_matrix)


def test_directed_distance_matrix_has_positive_distances() -> None:
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()
    nodes = build_network_nodes(stores, warehouse, suppliers)

    distance_matrix = build_directed_distance_matrix(nodes)

    assert all(entry.straight_line_distance_km > 0 for entry in distance_matrix)
    assert all(entry.estimated_road_distance_km is not None for entry in distance_matrix)
    assert all(entry.estimated_drive_minutes is not None for entry in distance_matrix)
