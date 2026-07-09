from datetime import date

from itara.sim import (
    MarkdownEvent,
    SaleEvent,
    SimulationEventType,
    SpoilageEvent,
    StockoutEvent,
    load_baseline_simulation_skus,
    simulate_baseline_day,
    summarize_events_by_type,
)

SIMULATION_DATE = date(2022, 1, 3)


def test_baseline_day_is_deterministic_for_same_date_and_seed() -> None:
    first_run = simulate_baseline_day(SIMULATION_DATE, seed=42)
    second_run = simulate_baseline_day(SIMULATION_DATE, seed=42)

    assert first_run == second_run


def test_baseline_simulation_skus_load_from_generated_catalog() -> None:
    skus = load_baseline_simulation_skus()

    assert [sku.sku_id for sku in skus] == ["sku_0001", "sku_0002"]
    assert all(sku.unit_cost > 0 for sku in skus)
    assert all(sku.unit_retail_price > sku.unit_cost for sku in skus)


def test_baseline_day_returns_small_non_empty_event_stream() -> None:
    events = simulate_baseline_day(SIMULATION_DATE)

    assert 10 <= len(events) <= 20
    assert all(event.event_date == SIMULATION_DATE for event in events)


def test_baseline_day_event_ids_are_unique() -> None:
    events = simulate_baseline_day(SIMULATION_DATE)
    event_ids = [event.event_id for event in events]

    assert len(event_ids) == len(set(event_ids))


def test_baseline_day_contains_required_event_types() -> None:
    events = simulate_baseline_day(SIMULATION_DATE)
    event_types = {event.event_type for event in events}

    assert {
        SimulationEventType.SALE,
        SimulationEventType.INVENTORY_COUNT,
        SimulationEventType.STOCKOUT,
        SimulationEventType.SPOILAGE,
        SimulationEventType.MARKDOWN,
    }.issubset(event_types)


def test_baseline_events_use_sku_ids_from_catalog() -> None:
    skus = load_baseline_simulation_skus()
    catalog_sku_ids = {sku.sku_id for sku in skus}
    events = simulate_baseline_day(SIMULATION_DATE)
    event_sku_ids = {
        event.sku_id
        for event in events
        if isinstance(
            event,
            SaleEvent | SpoilageEvent | StockoutEvent | MarkdownEvent,
        )
    }

    assert event_sku_ids == catalog_sku_ids


def test_baseline_events_use_catalog_price_and_cost_values() -> None:
    skus = load_baseline_simulation_skus()
    skus_by_id = {sku.sku_id: sku for sku in skus}
    events = simulate_baseline_day(SIMULATION_DATE)

    priced_events = [event for event in events if isinstance(event, SaleEvent | StockoutEvent)]
    assert priced_events
    for event in priced_events:
        sku = skus_by_id[event.sku_id]
        assert event.unit_cost == sku.unit_cost
        assert event.unit_retail_price == sku.unit_retail_price

    spoilage_event = next(event for event in events if isinstance(event, SpoilageEvent))
    assert spoilage_event.unit_cost == skus_by_id[spoilage_event.sku_id].unit_cost

    markdown_event = next(event for event in events if isinstance(event, MarkdownEvent))
    markdown_sku = skus_by_id[markdown_event.sku_id]
    assert markdown_event.original_unit_retail_price == markdown_sku.unit_retail_price
    assert markdown_event.markdown_unit_retail_price < markdown_sku.unit_retail_price


def test_summarize_events_by_type_returns_correct_counts() -> None:
    events = simulate_baseline_day(SIMULATION_DATE)

    assert summarize_events_by_type(events) == {
        "sale": 4,
        "stockout": 1,
        "spoilage": 1,
        "markdown": 1,
        "inventory_count": 6,
    }
