"""Simulation contracts for Itara Fresh Intelligence."""

from itara.sim.baseline import (
    load_baseline_simulation_skus,
    simulate_baseline_day,
    summarize_events_by_type,
)
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
from itara.sim.reports import (
    run_baseline_smoke_report,
    write_baseline_smoke_report,
)
from itara.sim.state import (
    InventoryPosition,
    NetworkDailyInventoryState,
    StoreDailyInventoryState,
    WarehouseDailyInventoryState,
)
from itara.sim.transitions import apply_event_to_state, apply_events_to_state

__all__ = [
    "BaseEvent",
    "FinancialImpactSummary",
    "InventoryCountEvent",
    "InventoryPosition",
    "MarkdownEvent",
    "NetworkDailyInventoryState",
    "SaleEvent",
    "SimulationEvent",
    "SimulationEventType",
    "SpoilageEvent",
    "StockoutEvent",
    "StoreDailyInventoryState",
    "StoreDeliveryEvent",
    "StoreTransferEvent",
    "SupplierDelayEvent",
    "SupplierShortShipmentEvent",
    "WarehouseDailyInventoryState",
    "WarehouseAllocationEvent",
    "WarehouseReceiptEvent",
    "apply_event_to_state",
    "apply_events_to_state",
    "calculate_holding_cost",
    "calculate_markdown_margin_loss",
    "calculate_net_loss",
    "calculate_spoilage_loss",
    "calculate_stockout_lost_margin",
    "calculate_transfer_cost",
    "load_baseline_simulation_skus",
    "run_baseline_smoke_report",
    "simulate_baseline_day",
    "summarize_daily_financial_impact",
    "summarize_events_by_type",
    "write_baseline_smoke_report",
]
