"""Small baseline replay runner for Phase 2 simulator foundation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from math import fsum

from itara.sim.baseline import (
    STORE_IDS,
    WAREHOUSE_ID,
    load_baseline_simulation_skus,
    simulate_baseline_day,
    summarize_events_by_type,
)
from itara.sim.events import BaseEvent, InventoryCountEvent
from itara.sim.financials import FinancialImpactSummary
from itara.sim.impact import summarize_daily_financial_impact
from itara.sim.state import (
    InventoryPosition,
    NetworkDailyInventoryState,
    StoreDailyInventoryState,
    WarehouseDailyInventoryState,
)
from itara.sim.transitions import apply_event_to_state

INITIAL_STORE_ON_HAND_UNITS = 120
INITIAL_WAREHOUSE_ON_HAND_UNITS = 500


@dataclass(frozen=True, slots=True)
class DailyReplayResult:
    """Inventory and financial summary for one replayed baseline day."""

    simulation_date: date
    event_counts: dict[str, int]
    skipped_state_event_counts: dict[str, int]
    financial_impact: FinancialImpactSummary
    ending_inventory_state: NetworkDailyInventoryState


@dataclass(frozen=True, slots=True)
class BaselineReplayResult:
    """Summary returned by the bounded baseline replay runner."""

    start_date: date
    end_date: date
    days: int
    seed: int
    daily_results: tuple[DailyReplayResult, ...]
    final_inventory_state: NetworkDailyInventoryState

    def total_modeled_net_loss(self) -> float:
        """Return total modeled net loss across all replayed days."""
        return fsum(result.financial_impact.net_loss for result in self.daily_results)


def _validate_days(days: int) -> None:
    """Ensure replay covers at least one simulated day."""
    if days <= 0:
        msg = "days must be greater than 0"
        raise ValueError(msg)


def _initial_position(
    *,
    state_date: date,
    node_id: str,
    sku_id: str,
    on_hand_units: int,
    unit_cost: float,
    unit_retail_price: float,
) -> InventoryPosition:
    """Build a deterministic initial SKU position for baseline replay."""
    return InventoryPosition(
        state_date=state_date,
        node_id=node_id,
        sku_id=sku_id,
        on_hand_units=on_hand_units,
        reserved_units=0,
        available_units=on_hand_units,
        expired_units=0,
        near_expiry_units=0,
        unit_cost=unit_cost,
        unit_retail_price=unit_retail_price,
        days_of_cover=None,
    )


def _create_initial_state(state_date: date) -> NetworkDailyInventoryState:
    """Create deterministic starting inventory for the baseline SKU slice."""
    skus = load_baseline_simulation_skus()

    warehouse_positions = tuple(
        _initial_position(
            state_date=state_date,
            node_id=WAREHOUSE_ID,
            sku_id=sku.sku_id,
            on_hand_units=INITIAL_WAREHOUSE_ON_HAND_UNITS,
            unit_cost=sku.unit_cost,
            unit_retail_price=sku.unit_retail_price,
        )
        for sku in skus
    )
    store_states = tuple(
        StoreDailyInventoryState(
            state_date=state_date,
            store_id=store_id,
            positions=tuple(
                _initial_position(
                    state_date=state_date,
                    node_id=store_id,
                    sku_id=sku.sku_id,
                    on_hand_units=INITIAL_STORE_ON_HAND_UNITS,
                    unit_cost=sku.unit_cost,
                    unit_retail_price=sku.unit_retail_price,
                )
                for sku in skus
            ),
        )
        for store_id in STORE_IDS
    )

    return NetworkDailyInventoryState(
        state_date=state_date,
        warehouse_state=WarehouseDailyInventoryState(
            state_date=state_date,
            warehouse_id=WAREHOUSE_ID,
            positions=warehouse_positions,
        ),
        store_states=store_states,
    )


def _advance_position_date(
    position: InventoryPosition,
    state_date: date,
) -> InventoryPosition:
    """Carry an inventory position forward to a new simulation date."""
    return InventoryPosition(**(position.model_dump() | {"state_date": state_date}))


def _advance_state_date(
    state: NetworkDailyInventoryState,
    state_date: date,
) -> NetworkDailyInventoryState:
    """Carry inventory quantities forward while updating daily state dates."""
    warehouse_state = WarehouseDailyInventoryState(
        state_date=state_date,
        warehouse_id=state.warehouse_state.warehouse_id,
        positions=tuple(
            _advance_position_date(position, state_date)
            for position in state.warehouse_state.positions
        ),
    )
    store_states = tuple(
        StoreDailyInventoryState(
            state_date=state_date,
            store_id=store_state.store_id,
            positions=tuple(
                _advance_position_date(position, state_date) for position in store_state.positions
            ),
        )
        for store_state in state.store_states
    )

    return NetworkDailyInventoryState(
        state_date=state_date,
        warehouse_state=warehouse_state,
        store_states=store_states,
    )


def _apply_replay_events(
    state: NetworkDailyInventoryState,
    events: tuple[BaseEvent, ...],
) -> tuple[NetworkDailyInventoryState, dict[str, int]]:
    """Apply replay-safe state transitions and count events skipped for state.

    The transition layer raises ``NotImplementedError`` for event types without
    tested state semantics. Replay keeps those events visible in counts and
    financial impact, but it does not mutate inventory state for them yet.

    Current baseline inventory counts are smoke-test observations, not
    state-aware reconciliation events. Applying them as authoritative counts
    can make the next day's generated sales impossible, so replay records them
    as skipped until the generator and reconciliation semantics are richer.
    """
    skipped_state_event_counts: Counter[str] = Counter()
    current_state = state

    for event in events:
        if isinstance(event, InventoryCountEvent):
            skipped_state_event_counts[event.event_type.value] += 1
            continue

        try:
            current_state = apply_event_to_state(current_state, event)
        except NotImplementedError:
            skipped_state_event_counts[event.event_type.value] += 1

    return current_state, dict(skipped_state_event_counts)


def run_baseline_replay(
    start_date: date,
    days: int = 7,
    seed: int = 42,
) -> BaselineReplayResult:
    """Replay a bounded baseline event stream into inventory and loss summaries."""
    _validate_days(days)

    state = _create_initial_state(start_date)
    daily_results: list[DailyReplayResult] = []

    for day_offset in range(days):
        simulation_date = start_date + timedelta(days=day_offset)
        state = _advance_state_date(state, simulation_date)
        events = simulate_baseline_day(
            simulation_date=simulation_date,
            seed=seed + day_offset,
        )
        state, skipped_state_event_counts = _apply_replay_events(
            state=state,
            events=events,
        )
        daily_results.append(
            DailyReplayResult(
                simulation_date=simulation_date,
                event_counts=summarize_events_by_type(events),
                skipped_state_event_counts=skipped_state_event_counts,
                financial_impact=summarize_daily_financial_impact(events),
                ending_inventory_state=state,
            )
        )

    return BaselineReplayResult(
        start_date=start_date,
        end_date=start_date + timedelta(days=days - 1),
        days=days,
        seed=seed,
        daily_results=tuple(daily_results),
        final_inventory_state=state,
    )
