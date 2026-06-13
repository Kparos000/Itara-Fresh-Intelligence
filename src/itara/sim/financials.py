"""Pure financial loss calculations for the operational simulator."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from itara.domain.exceptions import InvalidFinancialValueError


def _validate_non_negative(**values: float) -> None:
    """Validate that financial formula inputs are finite and non-negative."""
    for name, value in values.items():
        if not isfinite(value):
            msg = f"{name} must be finite"
            raise InvalidFinancialValueError(msg)
        if value < 0:
            msg = f"{name} must be non-negative"
            raise InvalidFinancialValueError(msg)


def calculate_spoilage_loss(expired_units: float, unit_cost: float) -> float:
    """Calculate inventory cost lost to spoilage."""
    _validate_non_negative(expired_units=expired_units, unit_cost=unit_cost)
    return expired_units * unit_cost


def calculate_stockout_lost_margin(
    unmet_demand_units: float,
    unit_retail_price: float,
    gross_margin_pct: float,
) -> float:
    """Calculate gross margin lost because demand could not be fulfilled."""
    _validate_non_negative(
        unmet_demand_units=unmet_demand_units,
        unit_retail_price=unit_retail_price,
        gross_margin_pct=gross_margin_pct,
    )
    if gross_margin_pct > 1:
        msg = "gross_margin_pct must not exceed 1"
        raise InvalidFinancialValueError(msg)

    return unmet_demand_units * unit_retail_price * gross_margin_pct


def calculate_markdown_margin_loss(
    markdown_units: float,
    margin_reduction_per_unit: float,
) -> float:
    """Calculate margin lost from selling units at a markdown."""
    _validate_non_negative(
        markdown_units=markdown_units,
        margin_reduction_per_unit=margin_reduction_per_unit,
    )
    return markdown_units * margin_reduction_per_unit


def calculate_transfer_cost(
    fixed_handling_cost: float,
    distance_km: float,
    cost_per_km: float,
) -> float:
    """Calculate fixed and distance-based store transfer cost."""
    _validate_non_negative(
        fixed_handling_cost=fixed_handling_cost,
        distance_km=distance_km,
        cost_per_km=cost_per_km,
    )
    return fixed_handling_cost + (distance_km * cost_per_km)


def calculate_holding_cost(
    excess_inventory_units: float,
    unit_cost: float,
    daily_holding_rate: float,
) -> float:
    """Calculate one day of holding cost for excess inventory."""
    _validate_non_negative(
        excess_inventory_units=excess_inventory_units,
        unit_cost=unit_cost,
        daily_holding_rate=daily_holding_rate,
    )
    return excess_inventory_units * unit_cost * daily_holding_rate


@dataclass(frozen=True, slots=True)
class FinancialImpactSummary:
    """Modeled loss components for a simulation period."""

    spoilage_loss: float
    stockout_lost_margin: float
    markdown_margin_loss: float
    transfer_cost: float
    holding_cost: float
    inference_cost: float
    net_loss: float

    def __post_init__(self) -> None:
        """Reject invalid summary values."""
        _validate_non_negative(
            spoilage_loss=self.spoilage_loss,
            stockout_lost_margin=self.stockout_lost_margin,
            markdown_margin_loss=self.markdown_margin_loss,
            transfer_cost=self.transfer_cost,
            holding_cost=self.holding_cost,
            inference_cost=self.inference_cost,
            net_loss=self.net_loss,
        )
        expected_net_loss = calculate_net_loss(
            spoilage_loss=self.spoilage_loss,
            stockout_lost_margin=self.stockout_lost_margin,
            markdown_margin_loss=self.markdown_margin_loss,
            transfer_cost=self.transfer_cost,
            holding_cost=self.holding_cost,
            inference_cost=self.inference_cost,
        )
        if not isclose(self.net_loss, expected_net_loss):
            msg = "net_loss must equal the sum of all financial impact components"
            raise InvalidFinancialValueError(msg)


def calculate_net_loss(
    spoilage_loss: float,
    stockout_lost_margin: float,
    markdown_margin_loss: float,
    transfer_cost: float,
    holding_cost: float,
    inference_cost: float,
) -> float:
    """Sum all modeled loss components."""
    _validate_non_negative(
        spoilage_loss=spoilage_loss,
        stockout_lost_margin=stockout_lost_margin,
        markdown_margin_loss=markdown_margin_loss,
        transfer_cost=transfer_cost,
        holding_cost=holding_cost,
        inference_cost=inference_cost,
    )
    return fsum(
        (
            spoilage_loss,
            stockout_lost_margin,
            markdown_margin_loss,
            transfer_cost,
            holding_cost,
            inference_cost,
        )
    )
