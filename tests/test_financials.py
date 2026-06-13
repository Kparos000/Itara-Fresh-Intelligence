import math
from collections.abc import Callable

import pytest

from itara.sim import (
    FinancialImpactSummary,
    calculate_holding_cost,
    calculate_markdown_margin_loss,
    calculate_net_loss,
    calculate_spoilage_loss,
    calculate_stockout_lost_margin,
    calculate_transfer_cost,
)


def test_financial_loss_formulas_are_correct() -> None:
    assert calculate_spoilage_loss(expired_units=12, unit_cost=2.5) == 30.0
    assert (
        calculate_stockout_lost_margin(
            unmet_demand_units=10,
            unit_retail_price=5.0,
            gross_margin_pct=0.4,
        )
        == 20.0
    )
    assert (
        calculate_markdown_margin_loss(
            markdown_units=8,
            margin_reduction_per_unit=0.75,
        )
        == 6.0
    )
    assert (
        calculate_transfer_cost(
            fixed_handling_cost=45.0,
            distance_km=10.0,
            cost_per_km=1.8,
        )
        == 63.0
    )
    assert (
        calculate_holding_cost(
            excess_inventory_units=100,
            unit_cost=2.0,
            daily_holding_rate=0.01,
        )
        == 2.0
    )


@pytest.mark.parametrize(
    ("calculation", "arguments", "invalid_field"),
    [
        (
            calculate_spoilage_loss,
            {"expired_units": -1.0, "unit_cost": 2.5},
            "expired_units",
        ),
        (
            calculate_stockout_lost_margin,
            {
                "unmet_demand_units": 10.0,
                "unit_retail_price": -5.0,
                "gross_margin_pct": 0.4,
            },
            "unit_retail_price",
        ),
        (
            calculate_markdown_margin_loss,
            {"markdown_units": 8.0, "margin_reduction_per_unit": -0.75},
            "margin_reduction_per_unit",
        ),
        (
            calculate_transfer_cost,
            {
                "fixed_handling_cost": 45.0,
                "distance_km": -10.0,
                "cost_per_km": 1.8,
            },
            "distance_km",
        ),
        (
            calculate_holding_cost,
            {
                "excess_inventory_units": 100.0,
                "unit_cost": 2.0,
                "daily_holding_rate": -0.01,
            },
            "daily_holding_rate",
        ),
        (
            calculate_net_loss,
            {
                "spoilage_loss": 30.0,
                "stockout_lost_margin": 20.0,
                "markdown_margin_loss": 6.0,
                "transfer_cost": 63.0,
                "holding_cost": 2.0,
                "inference_cost": -0.5,
            },
            "inference_cost",
        ),
    ],
)
def test_financial_calculations_reject_negative_inputs(
    calculation: Callable[..., object],
    arguments: dict[str, float],
    invalid_field: str,
) -> None:
    with pytest.raises(ValueError, match=invalid_field):
        calculation(**arguments)


def test_stockout_lost_margin_rejects_percentage_above_one() -> None:
    with pytest.raises(ValueError, match="gross_margin_pct"):
        calculate_stockout_lost_margin(
            unmet_demand_units=10,
            unit_retail_price=5.0,
            gross_margin_pct=1.01,
        )


def test_financial_calculations_reject_non_finite_inputs() -> None:
    with pytest.raises(ValueError, match="unit_cost must be finite"):
        calculate_spoilage_loss(expired_units=1, unit_cost=math.inf)


def test_net_loss_sums_all_components() -> None:
    net_loss = calculate_net_loss(
        spoilage_loss=30.0,
        stockout_lost_margin=20.0,
        markdown_margin_loss=6.0,
        transfer_cost=63.0,
        holding_cost=2.0,
        inference_cost=0.5,
    )

    assert net_loss == 121.5

    summary = FinancialImpactSummary(
        spoilage_loss=30.0,
        stockout_lost_margin=20.0,
        markdown_margin_loss=6.0,
        transfer_cost=63.0,
        holding_cost=2.0,
        inference_cost=0.5,
        net_loss=121.5,
    )
    assert summary.net_loss == net_loss


def test_zero_loss_case_returns_zero_summary() -> None:
    net_loss = calculate_net_loss(
        spoilage_loss=0.0,
        stockout_lost_margin=0.0,
        markdown_margin_loss=0.0,
        transfer_cost=0.0,
        holding_cost=0.0,
        inference_cost=0.0,
    )

    assert net_loss == 0.0

    summary = FinancialImpactSummary(
        spoilage_loss=0.0,
        stockout_lost_margin=0.0,
        markdown_margin_loss=0.0,
        transfer_cost=0.0,
        holding_cost=0.0,
        inference_cost=0.0,
        net_loss=0.0,
    )
    assert summary.net_loss == 0.0


def test_financial_summary_rejects_inconsistent_net_loss() -> None:
    with pytest.raises(ValueError, match="net_loss must equal"):
        FinancialImpactSummary(
            spoilage_loss=10.0,
            stockout_lost_margin=5.0,
            markdown_margin_loss=2.0,
            transfer_cost=3.0,
            holding_cost=1.0,
            inference_cost=0.5,
            net_loss=99.0,
        )
