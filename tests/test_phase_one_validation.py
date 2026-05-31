from pathlib import Path

from itara.validation import (
    phase_one_validation_payload,
    validate_phase_one_readiness,
    write_phase_one_validation_report,
)


def test_validate_phase_one_readiness_passes() -> None:
    summary = validate_phase_one_readiness()

    assert summary.passed is True
    assert summary.store_count == 15
    assert summary.supplier_count == 10
    assert summary.warehouse_count == 1
    assert summary.sku_count == 500
    assert summary.policy_document_count == 5
    assert summary.network_node_count == 26
    assert summary.distance_matrix_entry_count == 650
    assert summary.product_category_count == 8


def test_phase_one_validation_payload_returns_dictionary() -> None:
    payload = phase_one_validation_payload()

    assert payload["passed"] is True
    assert payload["store_count"] == 15
    assert payload["sku_count"] == 500


def test_write_phase_one_validation_report_creates_json(tmp_path: Path) -> None:
    output_path = tmp_path / "phase_one_validation_summary.json"

    written_path = write_phase_one_validation_report(output_path)

    assert written_path.exists()
    assert written_path == output_path
