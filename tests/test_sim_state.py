from datetime import date

import pytest
from pydantic import ValidationError

from itara.sim import (
    InventoryPosition,
    NetworkDailyInventoryState,
    StoreDailyInventoryState,
    WarehouseDailyInventoryState,
)

STATE_DATE = date(2022, 1, 3)


def make_position(
    node_id: str = "store_001",
    sku_id: str = "sku_0001",
    on_hand_units: int = 20,
    reserved_units: int = 3,
    available_units: int = 17,
    expired_units: int = 1,
    near_expiry_units: int = 4,
) -> InventoryPosition:
    return InventoryPosition(
        state_date=STATE_DATE,
        node_id=node_id,
        sku_id=sku_id,
        on_hand_units=on_hand_units,
        reserved_units=reserved_units,
        available_units=available_units,
        expired_units=expired_units,
        near_expiry_units=near_expiry_units,
        unit_cost=1.23,
        unit_retail_price=1.99,
        days_of_cover=2.5,
    )


def test_valid_inventory_position_can_be_created() -> None:
    position = make_position()

    assert position.state_date == STATE_DATE
    assert position.node_id == "store_001"
    assert position.sku_id == "sku_0001"
    assert position.on_hand_units == 20
    assert position.available_units == 17
    assert position.days_of_cover == 2.5


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("on_hand_units", -1),
        ("reserved_units", -1),
        ("available_units", -1),
        ("expired_units", -1),
        ("near_expiry_units", -1),
        ("unit_cost", -0.01),
        ("unit_retail_price", -0.01),
        ("days_of_cover", -0.01),
    ],
)
def test_inventory_position_rejects_negative_values(
    field_name: str,
    invalid_value: int | float,
) -> None:
    position_data = make_position().model_dump()
    position_data[field_name] = invalid_value

    with pytest.raises(ValidationError):
        InventoryPosition(**position_data)


def test_inventory_position_rejects_available_units_above_on_hand_units() -> None:
    with pytest.raises(ValidationError, match="available_units"):
        make_position(on_hand_units=10, available_units=11)


def test_store_daily_inventory_state_aggregates_positions() -> None:
    state = StoreDailyInventoryState(
        state_date=STATE_DATE,
        store_id="store_001",
        positions=(
            make_position(on_hand_units=20, available_units=17, expired_units=1),
            make_position(
                sku_id="sku_0002",
                on_hand_units=12,
                reserved_units=2,
                available_units=10,
                expired_units=0,
            ),
        ),
    )

    assert state.total_on_hand_units() == 32
    assert state.total_available_units() == 27
    assert state.total_expired_units() == 1


def test_store_state_rejects_position_for_different_store() -> None:
    with pytest.raises(ValidationError, match="node_id"):
        StoreDailyInventoryState(
            state_date=STATE_DATE,
            store_id="store_001",
            positions=(make_position(node_id="store_002"),),
        )


def test_warehouse_daily_inventory_state_aggregates_positions() -> None:
    state = WarehouseDailyInventoryState(
        state_date=STATE_DATE,
        warehouse_id="warehouse_001",
        positions=(
            make_position(
                node_id="warehouse_001",
                on_hand_units=100,
                reserved_units=20,
                available_units=80,
                expired_units=2,
            ),
            make_position(
                node_id="warehouse_001",
                sku_id="sku_0002",
                on_hand_units=75,
                reserved_units=5,
                available_units=70,
                expired_units=1,
            ),
        ),
    )

    assert state.total_on_hand_units() == 175
    assert state.total_available_units() == 150
    assert state.total_expired_units() == 3


def test_warehouse_state_rejects_position_for_different_warehouse() -> None:
    with pytest.raises(ValidationError, match="node_id"):
        WarehouseDailyInventoryState(
            state_date=STATE_DATE,
            warehouse_id="warehouse_001",
            positions=(make_position(node_id="warehouse_002"),),
        )


def test_warehouse_and_store_states_combine_into_network_daily_state() -> None:
    store_state = StoreDailyInventoryState(
        state_date=STATE_DATE,
        store_id="store_001",
        positions=(make_position(on_hand_units=20, available_units=17, expired_units=1),),
    )
    warehouse_state = WarehouseDailyInventoryState(
        state_date=STATE_DATE,
        warehouse_id="warehouse_001",
        positions=(
            make_position(
                node_id="warehouse_001",
                on_hand_units=100,
                reserved_units=20,
                available_units=80,
                expired_units=2,
            ),
        ),
    )

    network_state = NetworkDailyInventoryState(
        state_date=STATE_DATE,
        warehouse_state=warehouse_state,
        store_states=(store_state,),
    )

    assert network_state.total_on_hand_units() == 120
    assert network_state.total_available_units() == 97
    assert network_state.total_expired_units() == 3


def test_network_state_rejects_mismatched_dates() -> None:
    store_state = StoreDailyInventoryState(
        state_date=date(2022, 1, 4),
        store_id="store_001",
        positions=(),
    )
    warehouse_state = WarehouseDailyInventoryState(
        state_date=STATE_DATE,
        warehouse_id="warehouse_001",
        positions=(),
    )

    with pytest.raises(ValidationError, match="store_state state_date"):
        NetworkDailyInventoryState(
            state_date=STATE_DATE,
            warehouse_state=warehouse_state,
            store_states=(store_state,),
        )
