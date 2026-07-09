"""Small deterministic baseline event stream for one simulated day."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from datetime import UTC, date, datetime, time
from itertools import count
from random import Random

from itara.domain import SKU, load_generated_sku_catalog
from itara.sim.events import (
    BaseEvent,
    InventoryCountEvent,
    MarkdownEvent,
    SaleEvent,
    SpoilageEvent,
    StockoutEvent,
)

STORE_IDS = ("store_001", "store_004")
WAREHOUSE_ID = "warehouse_001"
BASELINE_SKU_COUNT = 2


def _event_id(simulation_date: date, sequence: int, event_name: str) -> str:
    """Build a stable event identifier for a simulated day."""
    return f"{simulation_date:%Y%m%d}-{sequence:03d}-{event_name}"


def load_baseline_simulation_skus() -> tuple[SKU, ...]:
    """Load the small deterministic SKU slice used by the baseline smoke simulation."""
    skus = load_generated_sku_catalog()
    if len(skus) < BASELINE_SKU_COUNT:
        msg = f"Generated SKU catalog must contain at least {BASELINE_SKU_COUNT} SKUs"
        raise ValueError(msg)

    return skus[:BASELINE_SKU_COUNT]


def _markdown_unit_price(sku: SKU) -> float:
    """Apply a fixed markdown to catalog retail price for the smoke simulation."""
    return round(sku.unit_retail_price * 0.75, 2)


def simulate_baseline_day(
    simulation_date: date,
    seed: int = 42,
) -> tuple[BaseEvent, ...]:
    """Generate a small deterministic baseline event stream for one day."""
    random = Random(seed)
    skus = load_baseline_simulation_skus()
    created_at = datetime.combine(simulation_date, time(23, 59), tzinfo=UTC)
    events: list[BaseEvent] = []
    event_sequence = count(1)

    def next_event_id(event_name: str) -> str:
        return _event_id(simulation_date, next(event_sequence), event_name)

    for store_id in STORE_IDS:
        for sku in skus:
            events.append(
                SaleEvent(
                    event_id=next_event_id("sale"),
                    event_date=simulation_date,
                    created_at=created_at,
                    store_id=store_id,
                    sku_id=sku.sku_id,
                    quantity_units=random.randint(5, 18),
                    unit_cost=sku.unit_cost,
                    unit_retail_price=sku.unit_retail_price,
                )
            )

    spoilage_sku = skus[0]
    markdown_sku = skus[1]

    events.extend(
        (
            StockoutEvent(
                event_id=next_event_id("stockout"),
                event_date=simulation_date,
                created_at=created_at,
                store_id="store_004",
                sku_id=markdown_sku.sku_id,
                quantity_units=random.randint(2, 6),
                unit_cost=markdown_sku.unit_cost,
                unit_retail_price=markdown_sku.unit_retail_price,
            ),
            SpoilageEvent(
                event_id=next_event_id("spoilage"),
                event_date=simulation_date,
                created_at=created_at,
                node_id="store_001",
                sku_id=spoilage_sku.sku_id,
                quantity_units=random.randint(1, 4),
                unit_cost=spoilage_sku.unit_cost,
            ),
            MarkdownEvent(
                event_id=next_event_id("markdown"),
                event_date=simulation_date,
                created_at=created_at,
                store_id="store_001",
                sku_id=markdown_sku.sku_id,
                quantity_units=random.randint(3, 8),
                original_unit_retail_price=markdown_sku.unit_retail_price,
                markdown_unit_retail_price=_markdown_unit_price(markdown_sku),
            ),
        )
    )

    for node_id in (*STORE_IDS, WAREHOUSE_ID):
        for sku in skus:
            events.append(
                InventoryCountEvent(
                    event_id=next_event_id("inventory-count"),
                    event_date=simulation_date,
                    created_at=created_at,
                    node_id=node_id,
                    sku_id=sku.sku_id,
                    quantity_units=random.randint(0, 120),
                )
            )

    return tuple(events)


def summarize_events_by_type(events: Iterable[BaseEvent]) -> dict[str, int]:
    """Count simulation events by their stable event type value."""
    return dict(Counter(event.event_type.value for event in events))
