"""Small event-to-inventory-state transition skeleton for Phase 2."""

from __future__ import annotations

from collections.abc import Iterable

from itara.sim.events import (
    BaseEvent,
    InventoryCountEvent,
    SaleEvent,
    SpoilageEvent,
)
from itara.sim.state import (
    InventoryPosition,
    NetworkDailyInventoryState,
    StoreDailyInventoryState,
    WarehouseDailyInventoryState,
)


def _updated_position(position: InventoryPosition, **changes: object) -> InventoryPosition:
    """Return a validated copy of an inventory position with selected changes."""
    position_data = position.model_dump()
    position_data.update(changes)
    return InventoryPosition(**position_data)


def _apply_sale_to_position(position: InventoryPosition, event: SaleEvent) -> InventoryPosition:
    """Reduce store inventory after a completed sale."""
    if event.quantity_units > position.on_hand_units:
        msg = "sale quantity would make on_hand_units negative"
        raise ValueError(msg)
    if event.quantity_units > position.available_units:
        msg = "sale quantity would make available_units negative"
        raise ValueError(msg)

    return _updated_position(
        position,
        on_hand_units=position.on_hand_units - event.quantity_units,
        available_units=position.available_units - event.quantity_units,
        unit_cost=event.unit_cost,
        unit_retail_price=event.unit_retail_price,
    )


def _apply_spoilage_to_position(
    position: InventoryPosition,
    event: SpoilageEvent,
) -> InventoryPosition:
    """Remove spoiled units from inventory and record them as expired."""
    if event.quantity_units > position.on_hand_units:
        msg = "spoilage quantity would make on_hand_units negative"
        raise ValueError(msg)
    if event.quantity_units > position.available_units:
        msg = "spoilage quantity would make available_units negative"
        raise ValueError(msg)

    return _updated_position(
        position,
        on_hand_units=position.on_hand_units - event.quantity_units,
        available_units=position.available_units - event.quantity_units,
        expired_units=position.expired_units + event.quantity_units,
        unit_cost=event.unit_cost,
    )


def _apply_inventory_count_to_position(
    position: InventoryPosition,
    event: InventoryCountEvent,
) -> InventoryPosition:
    """Set observed on-hand units and clamp available units to that count."""
    return _updated_position(
        position,
        on_hand_units=event.quantity_units,
        available_units=min(position.available_units, event.quantity_units),
    )


def _replace_position(
    positions: tuple[InventoryPosition, ...],
    sku_id: str,
    updated_position: InventoryPosition,
) -> tuple[InventoryPosition, ...]:
    """Replace one SKU position in an immutable positions tuple."""
    return tuple(
        updated_position if position.sku_id == sku_id else position for position in positions
    )


def _find_position(
    positions: tuple[InventoryPosition, ...],
    sku_id: str,
    node_id: str,
) -> InventoryPosition:
    """Find an inventory position by node and SKU."""
    for position in positions:
        if position.node_id == node_id and position.sku_id == sku_id:
            return position

    msg = f"No inventory position found for node_id={node_id!r}, sku_id={sku_id!r}"
    raise KeyError(msg)


def _apply_store_event(
    state: NetworkDailyInventoryState,
    store_id: str,
    sku_id: str,
    updated_position: InventoryPosition,
) -> NetworkDailyInventoryState:
    """Replace one store position and return a validated network state."""
    store_states: list[StoreDailyInventoryState] = []
    matched_store = False

    for store_state in state.store_states:
        if store_state.store_id != store_id:
            store_states.append(store_state)
            continue

        matched_store = True
        store_states.append(
            StoreDailyInventoryState(
                state_date=store_state.state_date,
                store_id=store_state.store_id,
                positions=_replace_position(
                    positions=store_state.positions,
                    sku_id=sku_id,
                    updated_position=updated_position,
                ),
            )
        )

    if not matched_store:
        msg = f"No store state found for store_id={store_id!r}"
        raise KeyError(msg)

    return NetworkDailyInventoryState(
        state_date=state.state_date,
        warehouse_state=state.warehouse_state,
        store_states=tuple(store_states),
    )


def _apply_warehouse_event(
    state: NetworkDailyInventoryState,
    sku_id: str,
    updated_position: InventoryPosition,
) -> NetworkDailyInventoryState:
    """Replace one warehouse position and return a validated network state."""
    warehouse_state = WarehouseDailyInventoryState(
        state_date=state.warehouse_state.state_date,
        warehouse_id=state.warehouse_state.warehouse_id,
        positions=_replace_position(
            positions=state.warehouse_state.positions,
            sku_id=sku_id,
            updated_position=updated_position,
        ),
    )
    return NetworkDailyInventoryState(
        state_date=state.state_date,
        warehouse_state=warehouse_state,
        store_states=state.store_states,
    )


def _apply_position_update(
    state: NetworkDailyInventoryState,
    node_id: str,
    sku_id: str,
    updated_position: InventoryPosition,
) -> NetworkDailyInventoryState:
    """Route a position update to a store or the warehouse."""
    if node_id == state.warehouse_state.warehouse_id:
        return _apply_warehouse_event(
            state=state,
            sku_id=sku_id,
            updated_position=updated_position,
        )

    return _apply_store_event(
        state=state,
        store_id=node_id,
        sku_id=sku_id,
        updated_position=updated_position,
    )


def apply_event_to_state(
    state: NetworkDailyInventoryState,
    event: BaseEvent,
) -> NetworkDailyInventoryState:
    """Apply one supported simulator event to network inventory state.

    This skeleton intentionally raises ``NotImplementedError`` for event types
    that do not yet have tested inventory transition semantics. That keeps
    unsupported behavior visible instead of silently mutating or ignoring state.
    """
    if event.event_date != state.state_date:
        msg = "event_date must match state_date"
        raise ValueError(msg)

    if isinstance(event, SaleEvent):
        position = _find_position(
            positions=next(
                store_state.positions
                for store_state in state.store_states
                if store_state.store_id == event.store_id
            ),
            sku_id=event.sku_id,
            node_id=event.store_id,
        )
        updated_position = _apply_sale_to_position(position, event)
        return _apply_store_event(
            state=state,
            store_id=event.store_id,
            sku_id=event.sku_id,
            updated_position=updated_position,
        )

    if isinstance(event, SpoilageEvent):
        positions = (
            state.warehouse_state.positions
            if event.node_id == state.warehouse_state.warehouse_id
            else next(
                store_state.positions
                for store_state in state.store_states
                if store_state.store_id == event.node_id
            )
        )
        position = _find_position(
            positions=positions,
            sku_id=event.sku_id,
            node_id=event.node_id,
        )
        updated_position = _apply_spoilage_to_position(position, event)
        return _apply_position_update(
            state=state,
            node_id=event.node_id,
            sku_id=event.sku_id,
            updated_position=updated_position,
        )

    if isinstance(event, InventoryCountEvent):
        positions = (
            state.warehouse_state.positions
            if event.node_id == state.warehouse_state.warehouse_id
            else next(
                store_state.positions
                for store_state in state.store_states
                if store_state.store_id == event.node_id
            )
        )
        position = _find_position(
            positions=positions,
            sku_id=event.sku_id,
            node_id=event.node_id,
        )
        updated_position = _apply_inventory_count_to_position(position, event)
        return _apply_position_update(
            state=state,
            node_id=event.node_id,
            sku_id=event.sku_id,
            updated_position=updated_position,
        )

    msg = f"Inventory transition is not implemented for event_type={event.event_type.value!r}"
    raise NotImplementedError(msg)


def apply_events_to_state(
    initial_state: NetworkDailyInventoryState,
    events: Iterable[BaseEvent],
) -> NetworkDailyInventoryState:
    """Apply supported simulator events to state in the provided order."""
    state = initial_state
    for event in events:
        state = apply_event_to_state(state, event)
    return state
