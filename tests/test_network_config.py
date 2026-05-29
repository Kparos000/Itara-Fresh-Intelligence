from itara.config import load_stores, load_suppliers, load_warehouse
from itara.domain import ProductCategory, StoreFormat


def test_load_stores_returns_fifteen_validated_stores() -> None:
    stores = load_stores()

    assert len(stores) == 15
    assert stores[0].store_id == "store_001"
    assert stores[0].store_format == StoreFormat.LARGE_URBAN
    assert stores[-1].store_id == "store_015"

    store_ids = {store.store_id for store in stores}
    assert len(store_ids) == 15


def test_store_network_has_expected_district_coverage() -> None:
    stores = load_stores()
    districts = {store.district for store in stores}

    assert districts == {
        "Old Toronto",
        "North York",
        "Scarborough",
        "Etobicoke",
        "York",
        "East York",
        "Mississauga",
    }


def test_load_warehouse_returns_validated_central_dc() -> None:
    warehouse = load_warehouse()

    assert warehouse.warehouse_id == "warehouse_001"
    assert warehouse.average_days_of_cover == 12
    assert warehouse.transfer_max_radius_km == 25.0
    assert warehouse.category_capacity_units[ProductCategory.PRODUCE] == 80_000


def test_load_suppliers_returns_ten_validated_suppliers() -> None:
    suppliers = load_suppliers()

    assert len(suppliers) == 10
    assert suppliers[0].supplier_id == "supplier_001"
    assert suppliers[-1].supplier_id == "supplier_010"

    supplier_ids = {supplier.supplier_id for supplier in suppliers}
    assert len(supplier_ids) == 10


def test_supplier_categories_cover_all_product_categories() -> None:
    suppliers = load_suppliers()

    covered_categories = {
        category for supplier in suppliers for category in supplier.categories_supplied
    }

    assert covered_categories == set(ProductCategory)


def test_every_store_has_nearest_store_references() -> None:
    stores = load_stores()
    store_ids = {store.store_id for store in stores}

    for store in stores:
        assert store.nearest_store_ids
        assert store.store_id not in store.nearest_store_ids
        assert set(store.nearest_store_ids).issubset(store_ids)
