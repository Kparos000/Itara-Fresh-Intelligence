"""Aggregate simulator events into modeled daily financial impact."""

from __future__ import annotations

from collections.abc import Iterable
from math import fsum

from itara.sim.events import (
    BaseEvent,
    MarkdownEvent,
    SpoilageEvent,
    StockoutEvent,
    StoreTransferEvent,
)
from itara.sim.financials import (
    FinancialImpactSummary,
    calculate_markdown_margin_loss,
    calculate_net_loss,
    calculate_spoilage_loss,
    calculate_stockout_lost_margin,
    calculate_transfer_cost,
)


def _gross_margin_pct(event: StockoutEvent) -> float:
    """Derive a non-negative gross margin percentage from a stockout event."""
    if event.unit_retail_price == 0:
        return 0.0

    margin_per_unit = max(event.unit_retail_price - event.unit_cost, 0.0)
    return margin_per_unit / event.unit_retail_price


def summarize_daily_financial_impact(
    events: Iterable[BaseEvent],
) -> FinancialImpactSummary:
    """Calculate modeled daily losses represented by supported event types."""
    spoilage_losses: list[float] = []
    stockout_losses: list[float] = []
    markdown_losses: list[float] = []
    transfer_costs: list[float] = []

    for event in events:
        if isinstance(event, SpoilageEvent):
            spoilage_losses.append(
                calculate_spoilage_loss(
                    expired_units=event.quantity_units,
                    unit_cost=event.unit_cost,
                )
            )
        elif isinstance(event, StockoutEvent):
            stockout_losses.append(
                calculate_stockout_lost_margin(
                    unmet_demand_units=event.quantity_units,
                    unit_retail_price=event.unit_retail_price,
                    gross_margin_pct=_gross_margin_pct(event),
                )
            )
        elif isinstance(event, MarkdownEvent):
            markdown_losses.append(
                calculate_markdown_margin_loss(
                    markdown_units=event.quantity_units,
                    margin_reduction_per_unit=(
                        event.original_unit_retail_price - event.markdown_unit_retail_price
                    ),
                )
            )
        elif isinstance(event, StoreTransferEvent):
            transfer_costs.append(
                calculate_transfer_cost(
                    fixed_handling_cost=event.transfer_cost,
                    distance_km=0.0,
                    cost_per_km=0.0,
                )
            )

    spoilage_loss = fsum(spoilage_losses)
    stockout_lost_margin = fsum(stockout_losses)
    markdown_margin_loss = fsum(markdown_losses)
    transfer_cost = fsum(transfer_costs)
    holding_cost = 0.0
    inference_cost = 0.0
    net_loss = calculate_net_loss(
        spoilage_loss=spoilage_loss,
        stockout_lost_margin=stockout_lost_margin,
        markdown_margin_loss=markdown_margin_loss,
        transfer_cost=transfer_cost,
        holding_cost=holding_cost,
        inference_cost=inference_cost,
    )

    return FinancialImpactSummary(
        spoilage_loss=spoilage_loss,
        stockout_lost_margin=stockout_lost_margin,
        markdown_margin_loss=markdown_margin_loss,
        transfer_cost=transfer_cost,
        holding_cost=holding_cost,
        inference_cost=inference_cost,
        net_loss=net_loss,
    )
