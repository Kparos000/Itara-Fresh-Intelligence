from datetime import date
from pathlib import Path

import pytest

from itara.sim import run_baseline_smoke_report, write_baseline_smoke_report

START_DATE = date(2022, 1, 3)


def test_report_contains_expected_headings_and_metrics() -> None:
    report = run_baseline_smoke_report(START_DATE, days=7, seed=42)

    assert "# Itara Fresh Baseline Simulation Smoke Report" in report
    assert "## Simulation window" in report
    assert "## Event summary" in report
    assert "### Event count by type" in report
    assert "## Modeled financial impact" in report
    assert "Total event count: 91" in report
    assert "Total spoilage loss:" in report
    assert "Total stockout lost margin:" in report
    assert "Total markdown margin loss:" in report
    assert "Total transfer cost:" in report
    assert "Total holding cost:" in report
    assert "Total inference cost:" in report
    assert "Total modeled net loss:" in report


def test_report_is_deterministic_for_same_inputs() -> None:
    first_report = run_baseline_smoke_report(START_DATE, days=7, seed=42)
    second_report = run_baseline_smoke_report(START_DATE, days=7, seed=42)

    assert first_report == second_report


def test_writer_creates_markdown_file(tmp_path: Path) -> None:
    output_path = tmp_path / "reports" / "baseline-smoke.md"

    written_path = write_baseline_smoke_report(
        output_path=output_path,
        start_date=START_DATE,
        days=3,
        seed=42,
    )

    assert written_path == output_path
    assert output_path.is_file()
    assert output_path.read_text(encoding="utf-8") == run_baseline_smoke_report(
        START_DATE,
        days=3,
        seed=42,
    )


@pytest.mark.parametrize("days", [0, -1, -7])
def test_report_rejects_invalid_days(days: int) -> None:
    with pytest.raises(ValueError, match="days must be greater than 0"):
        run_baseline_smoke_report(START_DATE, days=days)
