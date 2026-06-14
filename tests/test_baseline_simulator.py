from datetime import date

from itara.sim import (
    SimulationEventType,
    simulate_baseline_day,
    summarize_events_by_type,
)

SIMULATION_DATE = date(2022, 1, 3)


def test_baseline_day_is_deterministic_for_same_date_and_seed() -> None:
    first_run = simulate_baseline_day(SIMULATION_DATE, seed=42)
    second_run = simulate_baseline_day(SIMULATION_DATE, seed=42)

    assert first_run == second_run


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


def test_summarize_events_by_type_returns_correct_counts() -> None:
    events = simulate_baseline_day(SIMULATION_DATE)

    assert summarize_events_by_type(events) == {
        "sale": 4,
        "stockout": 1,
        "spoilage": 1,
        "markdown": 1,
        "inventory_count": 6,
    }
