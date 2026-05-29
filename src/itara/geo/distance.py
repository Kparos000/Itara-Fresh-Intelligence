"""Geospatial utilities for Itara Fresh Intelligence.

The Phase 1 geospatial layer intentionally uses deterministic straight-line
and estimated-road-distance calculations. Later phases can replace or enrich
these estimates with routing-engine data without changing the domain contracts.
"""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from itara.domain import (
    Coordinates,
    DistanceMatrixEntry,
    MapNode,
    NetworkNodeType,
    Store,
    Supplier,
    Warehouse,
)

EARTH_RADIUS_KM = 6371.0088
DEFAULT_ROAD_DISTANCE_MULTIPLIER = 1.25
DEFAULT_URBAN_SPEED_KMPH = 35.0


def calculate_haversine_distance_km(origin: Coordinates, destination: Coordinates) -> float:
    """Calculate straight-line distance between two coordinates in kilometres."""
    origin_latitude = radians(origin.latitude)
    origin_longitude = radians(origin.longitude)
    destination_latitude = radians(destination.latitude)
    destination_longitude = radians(destination.longitude)

    latitude_delta = destination_latitude - origin_latitude
    longitude_delta = destination_longitude - origin_longitude

    haversine_value = (
        sin(latitude_delta / 2) ** 2
        + cos(origin_latitude) * cos(destination_latitude) * sin(longitude_delta / 2) ** 2
    )

    return 2 * EARTH_RADIUS_KM * asin(sqrt(haversine_value))


def estimate_road_distance_km(
    straight_line_distance_km: float,
    multiplier: float = DEFAULT_ROAD_DISTANCE_MULTIPLIER,
) -> float:
    """Estimate road distance from straight-line distance.

    This is intentionally simple in Phase 1. It gives the simulator a stable
    distance contract before introducing richer routing data.
    """
    if straight_line_distance_km < 0:
        msg = "straight_line_distance_km must be non-negative"
        raise ValueError(msg)

    if multiplier < 1.0:
        msg = "road distance multiplier must be at least 1.0"
        raise ValueError(msg)

    return straight_line_distance_km * multiplier


def estimate_drive_minutes(
    road_distance_km: float,
    average_speed_kmph: float = DEFAULT_URBAN_SPEED_KMPH,
) -> float:
    """Estimate drive duration in minutes."""
    if road_distance_km < 0:
        msg = "road_distance_km must be non-negative"
        raise ValueError(msg)

    if average_speed_kmph <= 0:
        msg = "average_speed_kmph must be positive"
        raise ValueError(msg)

    return (road_distance_km / average_speed_kmph) * 60


def store_to_map_node(store: Store) -> MapNode:
    """Convert a store model into a map-ready network node."""
    return MapNode(
        node_id=store.store_id,
        node_type=NetworkNodeType.STORE,
        node_name=store.store_name,
        coordinates=store.coordinates,
        region=store.district,
        metadata={
            "store_format": store.store_format.value,
            "store_persona": store.store_persona,
            "footfall_index": store.footfall_index,
            "price_sensitivity_index": store.price_sensitivity_index,
            "cold_storage_capacity_units": store.cold_storage_capacity_units,
        },
    )


def warehouse_to_map_node(warehouse: Warehouse) -> MapNode:
    """Convert a warehouse model into a map-ready network node."""
    return MapNode(
        node_id=warehouse.warehouse_id,
        node_type=NetworkNodeType.WAREHOUSE,
        node_name=warehouse.warehouse_name,
        coordinates=warehouse.coordinates,
        region="Central Distribution",
        category_coverage=tuple(warehouse.category_capacity_units.keys()),
        metadata={
            "average_days_of_cover": warehouse.average_days_of_cover,
            "emergency_dispatch_allowed": warehouse.emergency_dispatch_allowed,
            "transfer_max_radius_km": warehouse.transfer_max_radius_km,
        },
    )


def supplier_to_map_node(supplier: Supplier) -> MapNode:
    """Convert a supplier model into a map-ready network node."""
    return MapNode(
        node_id=supplier.supplier_id,
        node_type=NetworkNodeType.SUPPLIER,
        node_name=supplier.supplier_name,
        coordinates=supplier.coordinates,
        region=supplier.supplier_warehouse_name,
        category_coverage=supplier.categories_supplied,
        metadata={
            "normal_lead_time_days": supplier.normal_lead_time_days,
            "emergency_delivery_allowed": supplier.emergency_delivery_allowed,
            "reliability_score": supplier.reliability_score,
            "minimum_order_value": supplier.minimum_order_value,
        },
    )


def build_network_nodes(
    stores: tuple[Store, ...],
    warehouse: Warehouse,
    suppliers: tuple[Supplier, ...],
) -> tuple[MapNode, ...]:
    """Build all map-ready network nodes."""
    nodes: list[MapNode] = [warehouse_to_map_node(warehouse)]
    nodes.extend(store_to_map_node(store) for store in stores)
    nodes.extend(supplier_to_map_node(supplier) for supplier in suppliers)
    return tuple(nodes)


def build_directed_distance_matrix(
    nodes: tuple[MapNode, ...],
) -> tuple[DistanceMatrixEntry, ...]:
    """Build a directed distance matrix between all distinct network nodes."""
    entries: list[DistanceMatrixEntry] = []

    for origin in nodes:
        for destination in nodes:
            if origin.node_id == destination.node_id:
                continue

            straight_line_distance_km = calculate_haversine_distance_km(
                origin.coordinates,
                destination.coordinates,
            )
            estimated_road_distance_km = estimate_road_distance_km(straight_line_distance_km)
            estimated_drive_minutes = estimate_drive_minutes(estimated_road_distance_km)

            entries.append(
                DistanceMatrixEntry(
                    origin_node_id=origin.node_id,
                    destination_node_id=destination.node_id,
                    straight_line_distance_km=round(straight_line_distance_km, 3),
                    estimated_road_distance_km=round(estimated_road_distance_km, 3),
                    estimated_drive_minutes=round(estimated_drive_minutes, 1),
                )
            )

    return tuple(entries)
