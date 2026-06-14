from datetime import UTC, date, datetime

import pytest

from itara.sim import (
    InventoryCountEvent,
    MarkdownEvent,
    SaleEvent,
    SpoilageEvent,
    StockoutEvent,
    StoreTransferEvent,
    simulate_baseline_day,
    summarize_daily_financial_impact,
)

EVENT_DATE = date(2022, 1, 3)
CREATED_AT = datetime(2022, 1, 3, 23, 59, tzinfo=UTC)


def test_empty_events_produce_zero_loss() -> None:
    summary = summarize_daily_financial_impact(())

    assert summary.spoilage_loss == 0.0
    assert summary.stockout_lost_margin == 0.0
    assert summary.markdown_margin_loss == 0.0
    assert summary.transfer_cost == 0.0
    assert summary.holding_cost == 0.0
    assert summary.inference_cost == 0.0
    assert summary.net_loss == 0.0


def test_spoilage_events_add_spoilage_loss() -> None:
    event = SpoilageEvent(
        event_id="spoilage-001",
        event_date=EVENT_DATE,
        created_at=CREATED_AT,
        node_id="store_001",
        sku_id="sku_0001",
        quantity_units=4,
        unit_cost=1.85,
    )

    summary = summarize_daily_financial_impact((event,))

    assert summary.spoilage_loss == pytest.approx(7.4)
    assert summary.net_loss == pytest.approx(7.4)


def test_stockout_events_add_lost_margin() -> None:
    event = StockoutEvent(
        event_id="stockout-001",
        event_date=EVENT_DATE,
        created_at=CREATED_AT,
        store_id="store_004",
        sku_id="sku_0002",
        quantity_units=5,
        unit_cost=2.0,
        unit_retail_price=5.0,
    )

    summary = summarize_daily_financial_impact((event,))

    assert summary.stockout_lost_margin == pytest.approx(15.0)
    assert summary.net_loss == pytest.approx(15.0)


def test_markdown_events_add_markdown_margin_loss() -> None:
    event = MarkdownEvent(
        event_id="markdown-001",
        event_date=EVENT_DATE,
        created_at=CREATED_AT,
        store_id="store_001",
        sku_id="sku_0002",
        quantity_units=6,
        original_unit_retail_price=6.49,
        markdown_unit_retail_price=4.49,
    )

    summary = summarize_daily_financial_impact((event,))

    assert summary.markdown_margin_loss == pytest.approx(12.0)
    assert summary.net_loss == pytest.approx(12.0)


def test_mixed_events_produce_correct_net_loss() -> None:
    events = (
        SaleEvent(
            event_id="sale-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_0001",
            quantity_units=10,
            unit_cost=2.0,
            unit_retail_price=5.0,
        ),
        InventoryCountEvent(
            event_id="count-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_0001",
            quantity_units=20,
        ),
        SpoilageEvent(
            event_id="spoilage-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            node_id="store_001",
            sku_id="sku_0001",
            quantity_units=4,
            unit_cost=2.0,
        ),
        StockoutEvent(
            event_id="stockout-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_004",
            sku_id="sku_0002",
            quantity_units=5,
            unit_cost=2.0,
            unit_retail_price=5.0,
        ),
        MarkdownEvent(
            event_id="markdown-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            store_id="store_001",
            sku_id="sku_0002",
            quantity_units=6,
            original_unit_retail_price=6.5,
            markdown_unit_retail_price=4.5,
        ),
        StoreTransferEvent(
            event_id="transfer-001",
            event_date=EVENT_DATE,
            created_at=CREATED_AT,
            source_store_id="store_001",
            target_store_id="store_004",
            sku_id="sku_0001",
            quantity_units=3,
            unit_cost=2.0,
            transfer_cost=25.0,
        ),
    )

    summary = summarize_daily_financial_impact(events)

    assert summary.spoilage_loss == pytest.approx(8.0)
    assert summary.stockout_lost_margin == pytest.approx(15.0)
    assert summary.markdown_margin_loss == pytest.approx(12.0)
    assert summary.transfer_cost == pytest.approx(25.0)
    assert summary.net_loss == pytest.approx(60.0)


def test_baseline_simulator_events_can_be_summarized() -> None:
    events = simulate_baseline_day(EVENT_DATE, seed=42)

    summary = summarize_daily_financial_impact(events)

    assert summary.spoilage_loss > 0.0
    assert summary.stockout_lost_margin > 0.0
    assert summary.markdown_margin_loss > 0.0
    assert summary.transfer_cost == 0.0
    assert summary.inference_cost == 0.0
    assert summary.net_loss > 0.0
