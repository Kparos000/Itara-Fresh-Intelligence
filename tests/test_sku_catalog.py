from collections import Counter
from pathlib import Path

from itara.config import load_suppliers
from itara.domain import (
    ANCHOR_SKU_NAMES,
    CATEGORY_TARGET_COUNTS,
    ProductCategory,
    generate_sku_catalog,
    load_generated_sku_catalog,
    write_sku_catalog,
)


def test_generate_sku_catalog_creates_500_skus() -> None:
    skus = generate_sku_catalog()

    assert len(skus) == 500


def test_generate_sku_catalog_matches_category_targets() -> None:
    skus = generate_sku_catalog()

    category_counts = Counter(sku.category for sku in skus)

    assert category_counts == CATEGORY_TARGET_COUNTS


def test_generate_sku_catalog_has_unique_ids() -> None:
    skus = generate_sku_catalog()

    sku_ids = {sku.sku_id for sku in skus}

    assert len(sku_ids) == 500


def test_generate_sku_catalog_includes_40_anchor_skus() -> None:
    skus = generate_sku_catalog()
    sku_names = {sku.sku_name for sku in skus}

    anchor_names = {
        anchor_name
        for category_anchor_names in ANCHOR_SKU_NAMES.values()
        for anchor_name in category_anchor_names
    }

    assert len(anchor_names) == 40
    assert anchor_names.issubset(sku_names)


def test_sku_suppliers_exist_in_supplier_config() -> None:
    skus = generate_sku_catalog()
    suppliers = load_suppliers()
    supplier_ids = {supplier.supplier_id for supplier in suppliers}

    assert {sku.supplier_id for sku in skus}.issubset(supplier_ids)


def test_sku_catalog_has_expected_perishable_characteristics() -> None:
    skus = generate_sku_catalog()

    assert all(sku.shelf_life_days <= 21 for sku in skus)
    assert all(sku.unit_retail_price > sku.unit_cost for sku in skus)
    assert all(sku.case_pack_size > 0 for sku in skus)


def test_sku_catalog_covers_all_product_categories() -> None:
    skus = generate_sku_catalog()

    categories = {sku.category for sku in skus}

    assert categories == set(ProductCategory)


def test_write_sku_catalog_creates_json_artifact(tmp_path: Path) -> None:
    output_path = tmp_path / "sku_catalog.json"

    written_path = write_sku_catalog(output_path)

    assert written_path.exists()
    assert written_path == output_path


def test_load_generated_sku_catalog_loads_json_artifact() -> None:
    skus = load_generated_sku_catalog()

    assert len(skus) == 500
    assert skus[0].sku_id == "sku_0001"
    assert skus[0].unit_retail_price == 1.99
    assert skus[0].unit_cost == 1.23
    assert skus[0].gross_margin_pct == 0.38
