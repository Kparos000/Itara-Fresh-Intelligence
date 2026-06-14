"""Small deterministic baseline event stream for one simulated day."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from datetime import UTC, date, datetime, time
from itertools import count
from random import Random

from itara.sim.events import (
    BaseEvent,
    InventoryCountEvent,
    MarkdownEvent,
    SaleEvent,
    SpoilageEvent,
    StockoutEvent,
)

STORE_IDS = ("store_001", "store_004")
SKU_IDS = ("sku_0001", "sku_0002")
WAREHOUSE_ID = "warehouse_001"


def _event_id(simulation_date: date, sequence: int, event_name: str) -> str:
    """Build a stable event identifier for a simulated day."""
    return f"{simulation_date:%Y%m%d}-{sequence:03d}-{event_name}"


def simulate_baseline_day(
    simulation_date: date,
    seed: int = 42,
) -> tuple[BaseEvent, ...]:
    """Generate a small deterministic baseline event stream for one day."""
    random = Random(seed)
    created_at = datetime.combine(simulation_date, time(23, 59), tzinfo=UTC)
    events: list[BaseEvent] = []
    event_sequence = count(1)

    def next_event_id(event_name: str) -> str:
        return _event_id(simulation_date, next(event_sequence), event_name)

    for store_id in STORE_IDS:
        for sku_id in SKU_IDS:
            events.append(
                SaleEvent(
                    event_id=next_event_id("sale"),
                    event_date=simulation_date,
                    created_at=created_at,
                    store_id=store_id,
                    sku_id=sku_id,
                    quantity_units=random.randint(5, 18),
                    unit_cost=round(random.uniform(1.2, 3.5), 2),
                    unit_retail_price=round(random.uniform(4.0, 7.5), 2),
                )
            )

    events.extend(
        (
            StockoutEvent(
                event_id=next_event_id("stockout"),
                event_date=simulation_date,
                created_at=created_at,
                store_id="store_004",
                sku_id="sku_0002",
                quantity_units=random.randint(2, 6),
                unit_cost=2.1,
                unit_retail_price=5.49,
            ),
            SpoilageEvent(
                event_id=next_event_id("spoilage"),
                event_date=simulation_date,
                created_at=created_at,
                node_id="store_001",
                sku_id="sku_0001",
                quantity_units=random.randint(1, 4),
                unit_cost=1.85,
            ),
            MarkdownEvent(
                event_id=next_event_id("markdown"),
                event_date=simulation_date,
                created_at=created_at,
                store_id="store_001",
                sku_id="sku_0002",
                quantity_units=random.randint(3, 8),
                original_unit_retail_price=6.49,
                markdown_unit_retail_price=4.49,
            ),
        )
    )

    for node_id in (*STORE_IDS, WAREHOUSE_ID):
        for sku_id in SKU_IDS:
            events.append(
                InventoryCountEvent(
                    event_id=next_event_id("inventory-count"),
                    event_date=simulation_date,
                    created_at=created_at,
                    node_id=node_id,
                    sku_id=sku_id,
                    quantity_units=random.randint(0, 120),
                )
            )

    return tuple(events)


def summarize_events_by_type(events: Iterable[BaseEvent]) -> dict[str, int]:
    """Count simulation events by their stable event type value."""
    return dict(Counter(event.event_type.value for event in events))
