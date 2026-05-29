"""Network configuration parsing.

This module converts static YAML configuration into validated domain models.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from itara.config.loaders import load_yaml_file
from itara.domain import Coordinates, Store, Supplier, Warehouse
from itara.utils import config_dir


def _coordinates_from_mapping(raw_item: dict[str, Any]) -> Coordinates:
    """Build coordinates from a flat YAML mapping."""
    return Coordinates(
        latitude=raw_item["latitude"],
        longitude=raw_item["longitude"],
    )


def _store_from_mapping(raw_store: dict[str, Any]) -> Store:
    """Build a validated store model from a YAML mapping."""
    return Store(
        store_id=raw_store["store_id"],
        store_name=raw_store["store_name"],
        district=raw_store["district"],
        coordinates=_coordinates_from_mapping(raw_store),
        store_format=raw_store["store_format"],
        store_persona=raw_store["store_persona"],
        footfall_index=raw_store["footfall_index"],
        price_sensitivity_index=raw_store["price_sensitivity_index"],
        prepared_foods_affinity=raw_store["prepared_foods_affinity"],
        fresh_produce_affinity=raw_store["fresh_produce_affinity"],
        markdown_response_index=raw_store["markdown_response_index"],
        cold_storage_capacity_units=raw_store["cold_storage_capacity_units"],
        receiving_window_start=raw_store["receiving_window_start"],
        receiving_window_end=raw_store["receiving_window_end"],
        nearest_store_ids=tuple(raw_store.get("nearest_store_ids", ())),
    )


def _warehouse_from_mapping(raw_warehouse: dict[str, Any]) -> Warehouse:
    """Build a validated warehouse model from a YAML mapping."""
    return Warehouse(
        warehouse_id=raw_warehouse["warehouse_id"],
        warehouse_name=raw_warehouse["warehouse_name"],
        coordinates=_coordinates_from_mapping(raw_warehouse),
        average_days_of_cover=raw_warehouse["average_days_of_cover"],
        morning_dispatch_time=raw_warehouse["morning_dispatch_time"],
        afternoon_dispatch_time=raw_warehouse["afternoon_dispatch_time"],
        emergency_dispatch_allowed=raw_warehouse["emergency_dispatch_allowed"],
        emergency_dispatch_fixed_cost=raw_warehouse["emergency_dispatch_fixed_cost"],
        transfer_max_radius_km=raw_warehouse["transfer_max_radius_km"],
        transfer_fixed_cost=raw_warehouse["transfer_fixed_cost"],
        transfer_cost_per_km=raw_warehouse["transfer_cost_per_km"],
        category_capacity_units=raw_warehouse["category_capacity_units"],
    )


def _supplier_from_mapping(raw_supplier: dict[str, Any]) -> Supplier:
    """Build a validated supplier model from a YAML mapping."""
    return Supplier(
        supplier_id=raw_supplier["supplier_id"],
        supplier_name=raw_supplier["supplier_name"],
        supplier_warehouse_name=raw_supplier["supplier_warehouse_name"],
        coordinates=_coordinates_from_mapping(raw_supplier),
        categories_supplied=tuple(raw_supplier["categories_supplied"]),
        normal_lead_time_days=raw_supplier["normal_lead_time_days"],
        emergency_delivery_allowed=raw_supplier["emergency_delivery_allowed"],
        emergency_delivery_fee=raw_supplier["emergency_delivery_fee"],
        reliability_score=raw_supplier["reliability_score"],
        minimum_order_value=raw_supplier["minimum_order_value"],
        normal_delivery_days=tuple(raw_supplier["normal_delivery_days"]),
    )


def load_stores(path: Path | None = None) -> tuple[Store, ...]:
    """Load and validate store configuration."""
    config_path = path or config_dir() / "stores.yaml"
    loaded = load_yaml_file(config_path)
    raw_stores = loaded.get("stores")

    if not isinstance(raw_stores, list):
        msg = f"stores.yaml must contain a 'stores' list: {config_path}"
        raise ValueError(msg)

    return tuple(_store_from_mapping(raw_store) for raw_store in raw_stores)


def load_warehouse(path: Path | None = None) -> Warehouse:
    """Load and validate warehouse configuration."""
    config_path = path or config_dir() / "warehouse.yaml"
    loaded = load_yaml_file(config_path)
    raw_warehouse = loaded.get("warehouse")

    if not isinstance(raw_warehouse, dict):
        msg = f"warehouse.yaml must contain a 'warehouse' mapping: {config_path}"
        raise ValueError(msg)

    return _warehouse_from_mapping(raw_warehouse)


def load_suppliers(path: Path | None = None) -> tuple[Supplier, ...]:
    """Load and validate supplier configuration."""
    config_path = path or config_dir() / "suppliers.yaml"
    loaded = load_yaml_file(config_path)
    raw_suppliers = loaded.get("suppliers")

    if not isinstance(raw_suppliers, list):
        msg = f"suppliers.yaml must contain a 'suppliers' list: {config_path}"
        raise ValueError(msg)

    return tuple(_supplier_from_mapping(raw_supplier) for raw_supplier in raw_suppliers)
