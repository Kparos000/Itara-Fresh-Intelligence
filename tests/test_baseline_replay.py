from datetime import date

import pytest

from itara.sim import (
    BaselineReplayResult,
    NetworkDailyInventoryState,
    run_baseline_replay,
)


def test_baseline_replay_is_deterministic_for_same_inputs() -> None:
    start_date = date(2022, 1, 3)

    first_result = run_baseline_replay(start_date=start_date, days=3, seed=42)
    second_result = run_baseline_replay(start_date=start_date, days=3, seed=42)

    assert first_result == second_result


def test_baseline_replay_daily_result_count_equals_days() -> None:
    result = run_baseline_replay(start_date=date(2022, 1, 3), days=5, seed=42)

    assert isinstance(result, BaselineReplayResult)
    assert len(result.daily_results) == 5
    assert result.end_date == date(2022, 1, 7)


def test_baseline_replay_returns_final_inventory_state() -> None:
    result = run_baseline_replay(start_date=date(2022, 1, 3), days=2, seed=42)

    assert isinstance(result.final_inventory_state, NetworkDailyInventoryState)
    assert result.final_inventory_state.state_date == date(2022, 1, 4)
    assert result.final_inventory_state.total_on_hand_units() >= 0


def test_baseline_replay_returns_daily_financial_impact() -> None:
    result = run_baseline_replay(start_date=date(2022, 1, 3), days=2, seed=42)

    assert all(daily.financial_impact.net_loss >= 0 for daily in result.daily_results)
    assert all(daily.event_counts for daily in result.daily_results)


def test_baseline_replay_total_modeled_net_loss_is_non_negative() -> None:
    result = run_baseline_replay(start_date=date(2022, 1, 3), days=7, seed=42)

    assert result.total_modeled_net_loss() >= 0


@pytest.mark.parametrize("days", [0, -1])
def test_baseline_replay_invalid_days_fail(days: int) -> None:
    with pytest.raises(ValueError, match="days must be greater than 0"):
        run_baseline_replay(start_date=date(2022, 1, 3), days=days, seed=42)
