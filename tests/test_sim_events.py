from datetime import UTC, date, datetime

import pytest
from pydantic import ValidationError

from itara.sim import (
    InventoryCountEvent,
    MarkdownEvent,
    SaleEvent,
    SimulationEventType,
    SpoilageEvent,
    StockoutEvent,
    StoreDeliveryEvent,
    StoreTransferEvent,
    SupplierDelayEvent,
    SupplierShortShipmentEvent,
    WarehouseAllocationEvent,
    WarehouseReceiptEvent,
)

EVENT_DATE = date(2022, 1, 3)
CREATED_AT = datetime(2022, 1, 3, 12, 0, tzinfo=UTC)


def test_all_simulation_events_can_be_instantiated() -> None:
    events = [
        SaleEvent(
            event_id="event_sale_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=4,
            unit_cost=1.2,
            unit_retail_price=1.99,
        ),
        WarehouseReceiptEvent(
            event_id="event_receipt_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            warehouse_id="warehouse_001",
            supplier_id="supplier_001",
            sku_id="sku_001",
            quantity_units=400,
            unit_cost=1.2,
        ),
        WarehouseAllocationEvent(
            event_id="event_allocation_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            warehouse_id="warehouse_001",
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=80,
            unit_cost=1.2,
        ),
        StoreDeliveryEvent(
            event_id="event_delivery_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            warehouse_id="warehouse_001",
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=80,
            unit_cost=1.2,
        ),
        InventoryCountEvent(
            event_id="event_count_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_001",
            quantity_units=76,
        ),
        SpoilageEvent(
            event_id="event_spoilage_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_001",
            quantity_units=3,
            unit_cost=1.2,
        ),
        StockoutEvent(
            event_id="event_stockout_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=7,
            unit_cost=1.2,
            unit_retail_price=1.99,
        ),
        MarkdownEvent(
            event_id="event_markdown_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=10,
            original_unit_retail_price=1.99,
            markdown_unit_retail_price=1.49,
        ),
        StoreTransferEvent(
            event_id="event_transfer_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            source_store_id="store_004",
            target_store_id="store_011",
            sku_id="sku_001",
            quantity_units=20,
            unit_cost=1.2,
            transfer_cost=62.5,
        ),
        SupplierDelayEvent(
            event_id="event_delay_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            supplier_id="supplier_001",
            warehouse_id="warehouse_001",
            sku_id="sku_001",
            quantity_units=400,
            delay_days=2,
        ),
        SupplierShortShipmentEvent(
            event_id="event_short_001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            supplier_id="supplier_001",
            warehouse_id="warehouse_001",
            sku_id="sku_001",
            expected_quantity_units=400,
            received_quantity_units=350,
            unit_cost=1.2,
        ),
    ]

    assert len(events) == 11
    assert all(event.event_date == EVENT_DATE for event in events)


@pytest.mark.parametrize(
    ("event_class", "event_data"),
    [
        (
            SaleEvent,
            {
                "store_id": "store_001",
                "sku_id": "sku_001",
                "quantity_units": -1,
                "unit_cost": 1.2,
                "unit_retail_price": 1.99,
            },
        ),
        (
            WarehouseReceiptEvent,
            {
                "warehouse_id": "warehouse_001",
                "supplier_id": "supplier_001",
                "sku_id": "sku_001",
                "quantity_units": -1,
                "unit_cost": 1.2,
            },
        ),
        (
            StoreTransferEvent,
            {
                "source_store_id": "store_004",
                "target_store_id": "store_011",
                "sku_id": "sku_001",
                "quantity_units": -1,
                "unit_cost": 1.2,
                "transfer_cost": 62.5,
            },
        ),
    ],
)
def test_events_reject_negative_quantities(
    event_class: type[SaleEvent | WarehouseReceiptEvent | StoreTransferEvent],
    event_data: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        event_class(
            event_id="event_invalid_quantity",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            **event_data,
        )


def test_event_types_are_stable_and_cannot_be_overridden() -> None:
    event = SaleEvent(
        event_id="event_sale_002",
        event_date=EVENT_DATE,
        created_at=CREATED_AT,
        store_id="store_001",
        sku_id="sku_001",
        quantity_units=1,
        unit_cost=1.2,
        unit_retail_price=1.99,
    )

    assert event.event_type is SimulationEventType.SALE
    assert event.model_dump(mode="json")["event_type"] == "sale"

    with pytest.raises(ValidationError):
        SaleEvent(
            event_id="event_sale_wrong_type",
            event_type=SimulationEventType.STOCKOUT,
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=1,
            unit_cost=1.2,
            unit_retail_price=1.99,
        )


@pytest.mark.parametrize(
    ("event_class", "event_data"),
    [
        (
            StockoutEvent,
            {
                "store_id": "store_001",
                "sku_id": "sku_001",
                "quantity_units": 1,
                "unit_cost": -0.01,
                "unit_retail_price": 1.99,
            },
        ),
        (
            MarkdownEvent,
            {
                "store_id": "store_001",
                "sku_id": "sku_001",
                "quantity_units": 1,
                "original_unit_retail_price": 1.99,
                "markdown_unit_retail_price": -0.01,
            },
        ),
        (
            StoreTransferEvent,
            {
                "source_store_id": "store_004",
                "target_store_id": "store_011",
                "sku_id": "sku_001",
                "quantity_units": 1,
                "unit_cost": 1.2,
                "transfer_cost": -0.01,
            },
        ),
    ],
)
def test_events_reject_negative_financial_fields(
    event_class: type[StockoutEvent | MarkdownEvent | StoreTransferEvent],
    event_data: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        event_class(
            event_id="event_invalid_financial",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            **event_data,
        )


def test_markdown_rejects_price_above_original_retail_price() -> None:
    with pytest.raises(ValidationError):
        MarkdownEvent(
            event_id="event_invalid_markdown",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_001",
            quantity_units=1,
            original_unit_retail_price=1.99,
            markdown_unit_retail_price=2.49,
        )


def test_store_transfer_requires_distinct_stores() -> None:
    with pytest.raises(ValidationError):
        StoreTransferEvent(
            event_id="event_invalid_transfer",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            source_store_id="store_004",
            target_store_id="store_004",
            sku_id="sku_001",
            quantity_units=1,
            unit_cost=1.2,
            transfer_cost=62.5,
        )


def test_short_shipment_rejects_received_quantity_above_expected() -> None:
    with pytest.raises(ValidationError):
        SupplierShortShipmentEvent(
            event_id="event_invalid_short_shipment",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            supplier_id="supplier_001",
            warehouse_id="warehouse_001",
            sku_id="sku_001",
            expected_quantity_units=400,
            received_quantity_units=401,
            unit_cost=1.2,
        )
