"""Simulation contracts for Itara Fresh Intelligence."""

from itara.sim.baseline import simulate_baseline_day, summarize_events_by_type
from itara.sim.events import (
    BaseEvent,
    InventoryCountEvent,
    MarkdownEvent,
    SaleEvent,
    SimulationEvent,
    SimulationEventType,
    SpoilageEvent,
    StockoutEvent,
    StoreDeliveryEvent,
    StoreTransferEvent,
    SupplierDelayEvent,
    SupplierShortShipmentEvent,
    WarehouseAllocationEvent,
    WarehouseReceiptEvent,
)
from itara.sim.financials import (
    FinancialImpactSummary,
    calculate_holding_cost,
    calculate_markdown_margin_loss,
    calculate_net_loss,
    calculate_spoilage_loss,
    calculate_stockout_lost_margin,
    calculate_transfer_cost,
)
from itara.sim.impact import summarize_daily_financial_impact

__all__ = [
    "BaseEvent",
    "FinancialImpactSummary",
    "InventoryCountEvent",
    "MarkdownEvent",
    "SaleEvent",
    "SimulationEvent",
    "SimulationEventType",
    "SpoilageEvent",
    "StockoutEvent",
    "StoreDeliveryEvent",
    "StoreTransferEvent",
    "SupplierDelayEvent",
    "SupplierShortShipmentEvent",
    "WarehouseAllocationEvent",
    "WarehouseReceiptEvent",
    "calculate_holding_cost",
    "calculate_markdown_margin_loss",
    "calculate_net_loss",
    "calculate_spoilage_loss",
    "calculate_stockout_lost_margin",
    "calculate_transfer_cost",
    "simulate_baseline_day",
    "summarize_daily_financial_impact",
    "summarize_events_by_type",
]
