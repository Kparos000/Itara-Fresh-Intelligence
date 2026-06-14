"""Small reproducible reports for baseline simulator smoke tests."""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from math import fsum
from pathlib import Path

from itara.sim.baseline import simulate_baseline_day, summarize_events_by_type
from itara.sim.impact import summarize_daily_financial_impact


def _validate_days(days: int) -> None:
    """Ensure a report covers at least one simulated day."""
    if days <= 0:
        msg = "days must be greater than 0"
        raise ValueError(msg)


def _format_currency(value: float) -> str:
    """Format a modeled financial value for the Markdown report."""
    return f"${value:,.2f}"


def run_baseline_smoke_report(
    start_date: date,
    days: int = 7,
    seed: int = 42,
) -> str:
    """Run a bounded multi-day baseline simulation and return Markdown."""
    _validate_days(days)

    event_counts: Counter[str] = Counter()
    daily_impacts = []
    total_event_count = 0

    for day_offset in range(days):
        simulation_date = start_date + timedelta(days=day_offset)
        events = simulate_baseline_day(
            simulation_date=simulation_date,
            seed=seed + day_offset,
        )
        event_counts.update(summarize_events_by_type(events))
        daily_impacts.append(summarize_daily_financial_impact(events))
        total_event_count += len(events)

    end_date = start_date + timedelta(days=days - 1)
    spoilage_loss = fsum(impact.spoilage_loss for impact in daily_impacts)
    stockout_lost_margin = fsum(impact.stockout_lost_margin for impact in daily_impacts)
    markdown_margin_loss = fsum(impact.markdown_margin_loss for impact in daily_impacts)
    transfer_cost = fsum(impact.transfer_cost for impact in daily_impacts)
    holding_cost = fsum(impact.holding_cost for impact in daily_impacts)
    inference_cost = fsum(impact.inference_cost for impact in daily_impacts)
    net_loss = fsum(impact.net_loss for impact in daily_impacts)

    event_count_lines = "\n".join(
        f"- `{event_type}`: {count}" for event_type, count in sorted(event_counts.items())
    )

    return (
        "# Itara Fresh Baseline Simulation Smoke Report\n\n"
        "This report summarizes modeled baseline losses from a small, "
        "deterministic simulation smoke test. It does not represent optimized "
        "operations, savings, or production results.\n\n"
        "## Simulation window\n\n"
        f"- Start date: {start_date.isoformat()}\n"
        f"- End date: {end_date.isoformat()}\n"
        f"- Simulated days: {days}\n"
        f"- Initial seed: {seed}\n\n"
        "## Event summary\n\n"
        f"- Total event count: {total_event_count}\n\n"
        "### Event count by type\n\n"
        f"{event_count_lines}\n\n"
        "## Modeled financial impact\n\n"
        f"- Total spoilage loss: {_format_currency(spoilage_loss)}\n"
        f"- Total stockout lost margin: {_format_currency(stockout_lost_margin)}\n"
        f"- Total markdown margin loss: {_format_currency(markdown_margin_loss)}\n"
        f"- Total transfer cost: {_format_currency(transfer_cost)}\n"
        f"- Total holding cost: {_format_currency(holding_cost)}\n"
        f"- Total inference cost: {_format_currency(inference_cost)}\n"
        f"- **Total modeled net loss: {_format_currency(net_loss)}**\n"
    )


def write_baseline_smoke_report(
    output_path: Path,
    start_date: date,
    days: int = 7,
    seed: int = 42,
) -> Path:
    """Write a baseline smoke report to the requested Markdown path."""
    report = run_baseline_smoke_report(
        start_date=start_date,
        days=days,
        seed=seed,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path
