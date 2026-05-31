"""Phase readiness validation for Itara Fresh Intelligence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from itara.config import load_stores, load_suppliers, load_warehouse
from itara.domain import CATEGORY_TARGET_COUNTS, ProductCategory, generate_sku_catalog
from itara.geo import build_directed_distance_matrix, build_network_nodes
from itara.rag import load_policy_documents
from itara.utils import generated_data_dir


@dataclass(frozen=True)
class PhaseOneValidationSummary:
    """Summary returned by the Phase 1 validation check."""

    store_count: int
    supplier_count: int
    warehouse_count: int
    sku_count: int
    policy_document_count: int
    network_node_count: int
    distance_matrix_entry_count: int
    product_category_count: int
    passed: bool


def validate_phase_one_readiness() -> PhaseOneValidationSummary:
    """Validate that Phase 1 core artifacts and contracts are healthy."""
    stores = load_stores()
    warehouse = load_warehouse()
    suppliers = load_suppliers()
    skus = generate_sku_catalog()
    policies = load_policy_documents()

    nodes = build_network_nodes(stores, warehouse, suppliers)
    distance_matrix = build_directed_distance_matrix(nodes)

    expected_sku_count = sum(CATEGORY_TARGET_COUNTS.values())
    expected_distance_entries = len(nodes) * (len(nodes) - 1)

    passed = (
        len(stores) == 15
        and warehouse.warehouse_id == "warehouse_001"
        and len(suppliers) == 10
        and len(skus) == expected_sku_count
        and len(policies) == 5
        and len(nodes) == 26
        and len(distance_matrix) == expected_distance_entries
        and set(ProductCategory) == {sku.category for sku in skus}
    )

    return PhaseOneValidationSummary(
        store_count=len(stores),
        supplier_count=len(suppliers),
        warehouse_count=1,
        sku_count=len(skus),
        policy_document_count=len(policies),
        network_node_count=len(nodes),
        distance_matrix_entry_count=len(distance_matrix),
        product_category_count=len(set(ProductCategory)),
        passed=passed,
    )


def write_phase_one_validation_report(output_path: Path | None = None) -> Path:
    """Write Phase 1 validation summary as JSON."""
    target_path = output_path or generated_data_dir() / "phase_one_validation_summary.json"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    summary = validate_phase_one_readiness()

    with target_path.open("w", encoding="utf-8") as file:
        json.dump(asdict(summary), file, indent=2, sort_keys=True)

    return target_path


def phase_one_validation_payload() -> dict[str, Any]:
    """Return Phase 1 validation summary as a dictionary."""
    return asdict(validate_phase_one_readiness())


def main() -> None:
    """Run Phase 1 validation from the command line."""
    summary = validate_phase_one_readiness()
    report_path = write_phase_one_validation_report()

    print(json.dumps(asdict(summary), indent=2, sort_keys=True))
    print(f"Wrote {report_path}")

    if not summary.passed:
        raise SystemExit(1)
