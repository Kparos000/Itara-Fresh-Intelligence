from datetime import date, time

import pytest
from pydantic import ValidationError

from itara.domain import (
    SKU,
    AgentDecisionTrace,
    Coordinates,
    DailyInventorySnapshot,
    DecisionAction,
    DistanceMatrixEntry,
    InventoryBatch,
    MapNode,
    NetworkNodeType,
    ProductCategory,
    RiskLevel,
    StorageType,
    Store,
    StoreFormat,
    Supplier,
    Warehouse,
)


def test_store_validates_receiving_window() -> None:
    store = Store(
        store_id="store_001",
        store_name="King West Fresh",
        district="Old Toronto",
        coordinates=Coordinates(latitude=43.6436, longitude=-79.4023),
        store_format=StoreFormat.LARGE_URBAN,
        store_persona="young_professionals",
        footfall_index=1.25,
        price_sensitivity_index=0.85,
        prepared_foods_affinity=1.45,
        fresh_produce_affinity=1.10,
        markdown_response_index=0.75,
        cold_storage_capacity_units=12_000,
        receiving_window_start=time(6, 0),
        receiving_window_end=time(11, 0),
        nearest_store_ids=("store_002", "store_003"),
    )

    assert store.store_id == "store_001"
    assert store.store_format == StoreFormat.LARGE_URBAN


def test_store_rejects_invalid_receiving_window() -> None:
    with pytest.raises(ValidationError):
        Store(
            store_id="store_001",
            store_name="King West Fresh",
            district="Old Toronto",
            coordinates=Coordinates(latitude=43.6436, longitude=-79.4023),
            store_format=StoreFormat.LARGE_URBAN,
            store_persona="young_professionals",
            footfall_index=1.25,
            price_sensitivity_index=0.85,
            prepared_foods_affinity=1.45,
            fresh_produce_affinity=1.10,
            markdown_response_index=0.75,
            cold_storage_capacity_units=12_000,
            receiving_window_start=time(11, 0),
            receiving_window_end=time(6, 0),
        )


def test_warehouse_requires_positive_category_capacity() -> None:
    warehouse = Warehouse(
        warehouse_id="warehouse_001",
        warehouse_name="Itara Central Fresh DC",
        coordinates=Coordinates(latitude=43.7418, longitude=-79.5294),
        average_days_of_cover=12,
        morning_dispatch_time=time(6, 0),
        afternoon_dispatch_time=time(13, 0),
        emergency_dispatch_allowed=True,
        emergency_dispatch_fixed_cost=275.0,
        transfer_max_radius_km=25.0,
        transfer_fixed_cost=45.0,
        transfer_cost_per_km=1.8,
        category_capacity_units={
            ProductCategory.PRODUCE: 80_000,
            ProductCategory.DAIRY: 60_000,
        },
    )

    assert warehouse.average_days_of_cover == 12
    assert warehouse.category_capacity_units[ProductCategory.PRODUCE] == 80_000


def test_supplier_requires_category_and_delivery_day() -> None:
    supplier = Supplier(
        supplier_id="supplier_001",
        supplier_name="Ontario Greenhouse Produce Co.",
        supplier_warehouse_name="Leamington Produce Hub",
        coordinates=Coordinates(latitude=42.0531, longitude=-82.5998),
        categories_supplied=(ProductCategory.PRODUCE,),
        normal_lead_time_days=2,
        emergency_delivery_allowed=True,
        emergency_delivery_fee=450.0,
        reliability_score=0.87,
        minimum_order_value=5_000.0,
        normal_delivery_days=("monday", "wednesday", "friday"),
    )

    assert supplier.categories_supplied == (ProductCategory.PRODUCE,)
    assert supplier.reliability_score == 0.87


def test_sku_validates_margin_and_cold_chain() -> None:
    sku = SKU(
        sku_id="sku_001",
        sku_name="Organic Bananas",
        category=ProductCategory.PRODUCE,
        subcategory="bananas",
        supplier_id="supplier_001",
        unit_retail_price=1.99,
        unit_cost=1.20,
        gross_margin_pct=0.40,
        shelf_life_days=5,
        case_pack_size=40,
        warehouse_case_pack_units=40,
        minimum_display_units=20,
        spoilage_rate_coefficient=1.15,
        substitution_group="banana",
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
    )

    assert sku.category == ProductCategory.PRODUCE
    assert sku.cold_chain_required is True


def test_sku_rejects_inconsistent_margin() -> None:
    with pytest.raises(ValidationError):
        SKU(
            sku_id="sku_001",
            sku_name="Organic Bananas",
            category=ProductCategory.PRODUCE,
            subcategory="bananas",
            supplier_id="supplier_001",
            unit_retail_price=1.99,
            unit_cost=1.20,
            gross_margin_pct=0.10,
            shelf_life_days=5,
            case_pack_size=40,
            warehouse_case_pack_units=40,
            minimum_display_units=20,
            spoilage_rate_coefficient=1.15,
            substitution_group="banana",
            storage_type=StorageType.CHILLED,
            cold_chain_required=True,
        )


def test_inventory_batch_rejects_unavailable_units_above_on_hand() -> None:
    with pytest.raises(ValidationError):
        InventoryBatch(
            batch_id="batch_001",
            sku_id="sku_001",
            node_id="warehouse_001",
            node_type=NetworkNodeType.WAREHOUSE,
            received_date=date(2025, 1, 1),
            expiry_date=date(2025, 1, 5),
            on_hand_units=100,
            reserved_units=80,
            quality_hold_units=30,
        )


def test_distance_matrix_entry_rejects_same_origin_and_destination() -> None:
    with pytest.raises(ValidationError):
        DistanceMatrixEntry(
            origin_node_id="store_001",
            destination_node_id="store_001",
            straight_line_distance_km=0.0,
        )


def test_map_node_supports_visualizer_contract() -> None:
    map_node = MapNode(
        node_id="store_001",
        node_type=NetworkNodeType.STORE,
        node_name="King West Fresh",
        coordinates=Coordinates(latitude=43.6436, longitude=-79.4023),
        region="Old Toronto",
        category_coverage=(ProductCategory.PRODUCE, ProductCategory.DAIRY),
        metadata={"store_format": "large_urban"},
    )

    assert map_node.node_type == NetworkNodeType.STORE
    assert map_node.metadata["store_format"] == "large_urban"


def test_daily_inventory_snapshot_validates_available_units() -> None:
    snapshot = DailyInventorySnapshot(
        snapshot_date=date(2025, 1, 1),
        node_id="store_001",
        sku_id="sku_001",
        on_hand_units=100,
        available_to_allocate_units=80,
        days_of_cover=3.5,
        stockout_risk=RiskLevel.LOW,
        spoilage_risk=RiskLevel.MEDIUM,
        overstock_risk=RiskLevel.LOW,
    )

    assert snapshot.days_of_cover == 3.5


def test_agent_decision_trace_phase_one_contract() -> None:
    trace = AgentDecisionTrace(
        trace_id="trace_001",
        decision_date=date(2025, 1, 1),
        node_id="store_001",
        recommended_action=DecisionAction.NO_ACTION,
        escalation_required=False,
        reason_codes=("no_risk_detected",),
    )

    assert trace.recommended_action == DecisionAction.NO_ACTION
    assert trace.reason_codes == ("no_risk_detected",)
