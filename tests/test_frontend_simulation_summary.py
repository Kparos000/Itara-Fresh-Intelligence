import json
from datetime import date

from itara.sim import write_frontend_simulation_summary


def test_frontend_simulation_summary_export_structure(tmp_path) -> None:
    output_path = tmp_path / "simulation-summary.json"

    written_path = write_frontend_simulation_summary(
        output_path=output_path,
        start_date=date(2022, 1, 3),
        days=2,
        seed=42,
    )

    payload = json.loads(written_path.read_text(encoding="utf-8"))

    assert written_path == output_path
    assert payload["start_date"] == "2022-01-03"
    assert payload["end_date"] == "2022-01-04"
    assert payload["days"] == 2
    assert payload["total_events"] == 26
    assert payload["event_counts"] == {
        "inventory_count": 12,
        "markdown": 2,
        "sale": 8,
        "spoilage": 2,
        "stockout": 2,
    }
    assert payload["total_net_loss"] >= 0
    assert len(payload["daily_net_loss"]) == 2
    assert set(payload["daily_net_loss"][0]) == {"date", "net_loss"}
