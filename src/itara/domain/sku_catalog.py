"""SKU catalog generation for Itara Fresh Intelligence.

The Phase 1 catalog combines named anchor SKUs with deterministic generated SKUs.
This keeps the demo realistic while preserving reproducibility for tests,
simulation, and future forecasting.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from itara.domain.models import SKU, ProductCategory, StorageType
from itara.utils import generated_data_dir


@dataclass(frozen=True)
class CategoryTemplate:
    """Template used to generate SKUs for one product category."""

    category: ProductCategory
    supplier_id: str
    subcategories: tuple[str, ...]
    storage_type: StorageType
    cold_chain_required: bool
    shelf_life_days: int
    retail_price_min: float
    retail_price_step: float
    gross_margin_pct: float
    case_pack_size: int
    minimum_display_units: int
    spoilage_rate_coefficient: float


CATEGORY_TARGET_COUNTS: dict[ProductCategory, int] = {
    ProductCategory.PRODUCE: 120,
    ProductCategory.DAIRY: 80,
    ProductCategory.MEAT: 70,
    ProductCategory.BAKERY: 60,
    ProductCategory.DELI: 50,
    ProductCategory.SEAFOOD: 40,
    ProductCategory.PREPARED_FOODS: 50,
    ProductCategory.FLORAL: 30,
}


CATEGORY_TEMPLATES: dict[ProductCategory, CategoryTemplate] = {
    ProductCategory.PRODUCE: CategoryTemplate(
        category=ProductCategory.PRODUCE,
        supplier_id="supplier_001",
        subcategories=("bananas", "berries", "leafy_greens", "tomatoes", "root_vegetables"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=5,
        retail_price_min=1.99,
        retail_price_step=0.35,
        gross_margin_pct=0.38,
        case_pack_size=24,
        minimum_display_units=18,
        spoilage_rate_coefficient=1.20,
    ),
    ProductCategory.DAIRY: CategoryTemplate(
        category=ProductCategory.DAIRY,
        supplier_id="supplier_003",
        subcategories=("milk", "yogurt", "cheese", "cream", "butter"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=18,
        retail_price_min=3.49,
        retail_price_step=0.40,
        gross_margin_pct=0.28,
        case_pack_size=12,
        minimum_display_units=10,
        spoilage_rate_coefficient=0.75,
    ),
    ProductCategory.MEAT: CategoryTemplate(
        category=ProductCategory.MEAT,
        supplier_id="supplier_004",
        subcategories=("chicken", "beef", "pork", "turkey", "halal_meat"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=4,
        retail_price_min=6.99,
        retail_price_step=0.75,
        gross_margin_pct=0.31,
        case_pack_size=8,
        minimum_display_units=6,
        spoilage_rate_coefficient=1.35,
    ),
    ProductCategory.BAKERY: CategoryTemplate(
        category=ProductCategory.BAKERY,
        supplier_id="supplier_006",
        subcategories=("bread", "pastries", "bagels", "cakes", "flatbreads"),
        storage_type=StorageType.AMBIENT,
        cold_chain_required=False,
        shelf_life_days=3,
        retail_price_min=2.99,
        retail_price_step=0.30,
        gross_margin_pct=0.43,
        case_pack_size=16,
        minimum_display_units=12,
        spoilage_rate_coefficient=1.45,
    ),
    ProductCategory.DELI: CategoryTemplate(
        category=ProductCategory.DELI,
        supplier_id="supplier_007",
        subcategories=("sliced_meats", "prepared_salads", "dips", "cheese_trays", "olives"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=10,
        retail_price_min=4.99,
        retail_price_step=0.45,
        gross_margin_pct=0.32,
        case_pack_size=10,
        minimum_display_units=8,
        spoilage_rate_coefficient=0.95,
    ),
    ProductCategory.SEAFOOD: CategoryTemplate(
        category=ProductCategory.SEAFOOD,
        supplier_id="supplier_008",
        subcategories=("salmon", "shrimp", "cod", "mussels", "seafood_mix"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=2,
        retail_price_min=8.99,
        retail_price_step=0.95,
        gross_margin_pct=0.35,
        case_pack_size=6,
        minimum_display_units=4,
        spoilage_rate_coefficient=1.60,
    ),
    ProductCategory.PREPARED_FOODS: CategoryTemplate(
        category=ProductCategory.PREPARED_FOODS,
        supplier_id="supplier_009",
        subcategories=("ready_meals", "salads", "soups", "sandwiches", "family_meals"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=2,
        retail_price_min=5.99,
        retail_price_step=0.55,
        gross_margin_pct=0.45,
        case_pack_size=8,
        minimum_display_units=6,
        spoilage_rate_coefficient=1.70,
    ),
    ProductCategory.FLORAL: CategoryTemplate(
        category=ProductCategory.FLORAL,
        supplier_id="supplier_010",
        subcategories=("bouquets", "roses", "seasonal", "plants", "arrangements"),
        storage_type=StorageType.CHILLED,
        cold_chain_required=True,
        shelf_life_days=6,
        retail_price_min=9.99,
        retail_price_step=1.25,
        gross_margin_pct=0.52,
        case_pack_size=6,
        minimum_display_units=4,
        spoilage_rate_coefficient=1.10,
    ),
}


ANCHOR_SKU_NAMES: dict[ProductCategory, tuple[str, ...]] = {
    ProductCategory.PRODUCE: (
        "Organic Bananas",
        "Ontario Strawberries",
        "Baby Spinach Clamshell",
        "Roma Tomatoes",
        "Sweet Potatoes",
    ),
    ProductCategory.DAIRY: (
        "2 Percent Milk 4L",
        "Greek Yogurt Plain",
        "Cheddar Cheese Block",
        "Whipping Cream",
        "Salted Butter",
    ),
    ProductCategory.MEAT: (
        "Chicken Breast Family Pack",
        "Lean Ground Beef",
        "Pork Tenderloin",
        "Turkey Cutlets",
        "Halal Chicken Thighs",
    ),
    ProductCategory.BAKERY: (
        "Sourdough Loaf",
        "Butter Croissants",
        "Everything Bagels",
        "Chocolate Cake Slice",
        "Garlic Naan",
    ),
    ProductCategory.DELI: (
        "Black Forest Ham",
        "Potato Salad",
        "Roasted Garlic Hummus",
        "Cheese Party Tray",
        "Marinated Olives",
    ),
    ProductCategory.SEAFOOD: (
        "Atlantic Salmon Fillet",
        "Cooked Shrimp Ring",
        "Fresh Cod Loins",
        "PEI Mussels",
        "Seafood Chowder Mix",
    ),
    ProductCategory.PREPARED_FOODS: (
        "Chicken Alfredo Meal",
        "Greek Salad Bowl",
        "Tomato Basil Soup",
        "Turkey Club Sandwich",
        "Family Lasagna Tray",
    ),
    ProductCategory.FLORAL: (
        "Mixed Spring Bouquet",
        "Red Rose Bunch",
        "Seasonal Tulips",
        "Mini Orchid Plant",
        "Premium Floral Arrangement",
    ),
}


def _unit_cost_from_margin(unit_retail_price: float, gross_margin_pct: float) -> float:
    """Calculate unit cost from retail price and margin."""
    return round(unit_retail_price * (1 - gross_margin_pct), 2)


def _build_sku(
    sku_number: int,
    sku_name: str,
    template: CategoryTemplate,
    sequence_in_category: int,
) -> SKU:
    """Build a validated SKU from template values."""
    retail_price = round(
        template.retail_price_min + (sequence_in_category % 11) * template.retail_price_step,
        2,
    )

    subcategory = template.subcategories[sequence_in_category % len(template.subcategories)]
    substitution_group = f"{template.category.value}_{subcategory}"

    return SKU(
        sku_id=f"sku_{sku_number:04d}",
        sku_name=sku_name,
        category=template.category,
        subcategory=subcategory,
        supplier_id=template.supplier_id,
        unit_retail_price=retail_price,
        unit_cost=_unit_cost_from_margin(retail_price, template.gross_margin_pct),
        gross_margin_pct=template.gross_margin_pct,
        shelf_life_days=template.shelf_life_days,
        case_pack_size=template.case_pack_size,
        warehouse_case_pack_units=template.case_pack_size,
        minimum_display_units=template.minimum_display_units,
        spoilage_rate_coefficient=template.spoilage_rate_coefficient,
        substitution_group=substitution_group,
        storage_type=template.storage_type,
        cold_chain_required=template.cold_chain_required,
    )


def generate_sku_catalog() -> tuple[SKU, ...]:
    """Generate the deterministic 500-SKU product catalog."""
    skus: list[SKU] = []
    sku_number = 1

    for category, target_count in CATEGORY_TARGET_COUNTS.items():
        template = CATEGORY_TEMPLATES[category]
        anchor_names = ANCHOR_SKU_NAMES[category]

        for sequence_in_category in range(target_count):
            if sequence_in_category < len(anchor_names):
                sku_name = anchor_names[sequence_in_category]
            else:
                subcategory = template.subcategories[
                    sequence_in_category % len(template.subcategories)
                ]
                sku_name = (
                    f"Itara {subcategory.replace('_', ' ').title()} Item {sequence_in_category + 1}"
                )

            skus.append(
                _build_sku(
                    sku_number=sku_number,
                    sku_name=sku_name,
                    template=template,
                    sequence_in_category=sequence_in_category,
                )
            )
            sku_number += 1

    return tuple(skus)


def write_sku_catalog(output_path: Path | None = None) -> Path:
    """Write the deterministic SKU catalog to JSON."""
    target_path = output_path or generated_data_dir() / "sku_catalog.json"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    skus = generate_sku_catalog()

    with target_path.open("w", encoding="utf-8") as file:
        json.dump([sku.model_dump(mode="json") for sku in skus], file, indent=2)

    return target_path


def main() -> None:
    """Generate the SKU catalog from the command line."""
    path = write_sku_catalog()
    print(f"Wrote {path}")
