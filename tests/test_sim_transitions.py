from datetime import UTC, date, datetime

import pytest

from itara.sim import (
    InventoryCountEvent,
    InventoryPosition,
    MarkdownEvent,
    NetworkDailyInventoryState,
    SaleEvent,
    SpoilageEvent,
    StoreDailyInventoryState,
    WarehouseDailyInventoryState,
    apply_event_to_state,
    apply_events_to_state,
)

STATE_DATE = date(2022, 1, 3)
CREATED_AT = datetime(2022, 1, 3, 12, 0, tzinfo=UTC)


def make_position(
    node_id: str,
    sku_id: str = "sku_0001",
    on_hand_units: int = 20,
    available_units: int = 18,
    expired_units: int = 0,
) -> InventoryPosition:
    return InventoryPosition(
        state_date=STATE_DATE,
        node_id=node_id,
        sku_id=sku_id,
        on_hand_units=on_hand_units,
        reserved_units=on_hand_units - available_units,
        available_units=available_units,
        expired_units=expired_units,
        near_expiry_units=2,
        unit_cost=1.23,
        unit_retail_price=1.99,
        days_of_cover=3.0,
    )


def make_network_state() -> NetworkDailyInventoryState:
    return NetworkDailyInventoryState(
        state_date=STATE_DATE,
        warehouse_state=WarehouseDailyInventoryState(
            state_date=STATE_DATE,
            warehouse_id="warehouse_001",
            positions=(make_position(node_id="warehouse_001", on_hand_units=100),),
        ),
        store_states=(
            StoreDailyInventoryState(
                state_date=STATE_DATE,
                store_id="store_001",
                positions=(make_position(node_id="store_001"),),
            ),
        ),
    )


def test_sale_event_reduces_store_inventory() -> None:
    state = make_network_state()
    event = SaleEvent(
        event_id="sale-001",
        event_date=STATE_DATE,
        created_at=CREATED_AT,
        store_id="store_001",
        sku_id="sku_0001",
        quantity_units=5,
        unit_cost=1.23,
        unit_retail_price=1.99,
    )

    updated_state = apply_event_to_state(state, event)
    position = updated_state.store_states[0].positions[0]

    assert position.on_hand_units == 15
    assert position.available_units == 13
    assert position.expired_units == 0


def test_spoilage_event_reduces_inventory_and_records_expired_units() -> None:
    state = make_network_state()
    event = SpoilageEvent(
        event_id="spoilage-001",
        event_date=STATE_DATE,
        created_at=CREATED_AT,
        node_id="store_001",
        sku_id="sku_0001",
        quantity_units=4,
        unit_cost=1.23,
    )

    updated_state = apply_event_to_state(state, event)
    position = updated_state.store_states[0].positions[0]

    assert position.on_hand_units == 16
    assert position.available_units == 14
    assert position.expired_units == 4


def test_inventory_count_sets_on_hand_and_clamps_available_units() -> None:
    state = make_network_state()
    event = InventoryCountEvent(
        event_id="count-001",
        event_date=STATE_DATE,
        created_at=CREATED_AT,
        node_id="store_001",
        sku_id="sku_0001",
        quantity_units=12,
    )

    updated_state = apply_event_to_state(state, event)
    position = updated_state.store_states[0].positions[0]

    assert position.on_hand_units == 12
    assert position.available_units == 12


def test_negative_inventory_transition_is_rejected() -> None:
    state = make_network_state()
    event = SaleEvent(
        event_id="sale-001",
        event_date=STATE_DATE,
        created_at=CREATED_AT,
        store_id="store_001",
        sku_id="sku_0001",
        quantity_units=25,
        unit_cost=1.23,
        unit_retail_price=1.99,
    )

    with pytest.raises(ValueError, match="on_hand_units"):
        apply_event_to_state(state, event)


def test_applying_multiple_events_is_deterministic() -> None:
    state = make_network_state()
    events = (
        SaleEvent(
            event_id="sale-001",
            event_date=STATE_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_0001",
            quantity_units=5,
            unit_cost=1.23,
            unit_retail_price=1.99,
        ),
        SpoilageEvent(
            event_id="spoilage-001",
            event_date=STATE_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_0001",
            quantity_units=3,
            unit_cost=1.23,
        ),
        InventoryCountEvent(
            event_id="count-001",
            event_date=STATE_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_0001",
            quantity_units=11,
        ),
    )

    first_run = apply_events_to_state(state, events)
    second_run = apply_events_to_state(state, events)

    assert first_run == second_run
    position = first_run.store_states[0].positions[0]
    assert position.on_hand_units == 11
    assert position.available_units == 10
    assert position.expired_units == 3


def test_unsupported_event_type_raises_not_implemented() -> None:
    state = make_network_state()
    event = MarkdownEvent(
        event_id="markdown-001",
        event_date=STATE_DATE,
        created_at=CREATED_AT,
        store_id="store_001",
        sku_id="sku_0001",
        quantity_units=2,
        original_unit_retail_price=1.99,
        markdown_unit_retail_price=1.49,
    )

    with pytest.raises(NotImplementedError, match="not implemented"):
        apply_event_to_state(state, event)
