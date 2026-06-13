"""Event contracts for the replayable operational simulator."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SimulationEventType(StrEnum):
    """Stable event names written to the simulator event stream."""

    SALE = "sale"
    WAREHOUSE_RECEIPT = "warehouse_receipt"
    WAREHOUSE_ALLOCATION = "warehouse_allocation"
    STORE_DELIVERY = "store_delivery"
    INVENTORY_COUNT = "inventory_count"
    SPOILAGE = "spoilage"
    STOCKOUT = "stockout"
    MARKDOWN = "markdown"
    STORE_TRANSFER = "store_transfer"
    SUPPLIER_DELAY = "supplier_delay"
    SUPPLIER_SHORT_SHIPMENT = "supplier_short_shipment"


class SimulationEvent(BaseModel):
    """Fields shared by every simulator event."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(..., min_length=3)
    event_type: SimulationEventType
    event_date: date
    created_at: datetime


class SaleEvent(SimulationEvent):
    """Completed customer sale at a store."""

    event_type: Literal[SimulationEventType.SALE] = SimulationEventType.SALE
    store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)
    unit_retail_price: float = Field(..., ge=0.0)


class WarehouseReceiptEvent(SimulationEvent):
    """Bulk supplier inventory received by the central warehouse."""

    event_type: Literal[SimulationEventType.WAREHOUSE_RECEIPT] = (
        SimulationEventType.WAREHOUSE_RECEIPT
    )
    warehouse_id: str = Field(..., min_length=3)
    supplier_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)


class WarehouseAllocationEvent(SimulationEvent):
    """Warehouse inventory reserved for a store replenishment."""

    event_type: Literal[SimulationEventType.WAREHOUSE_ALLOCATION] = (
        SimulationEventType.WAREHOUSE_ALLOCATION
    )
    warehouse_id: str = Field(..., min_length=3)
    store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)


class StoreDeliveryEvent(SimulationEvent):
    """Warehouse allocation delivered to a store."""

    event_type: Literal[SimulationEventType.STORE_DELIVERY] = SimulationEventType.STORE_DELIVERY
    warehouse_id: str = Field(..., min_length=3)
    store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)


class InventoryCountEvent(SimulationEvent):
    """Observed on-hand inventory at a store or warehouse."""

    event_type: Literal[SimulationEventType.INVENTORY_COUNT] = SimulationEventType.INVENTORY_COUNT
    node_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., ge=0)


class SpoilageEvent(SimulationEvent):
    """Inventory removed because it expired or failed freshness standards."""

    event_type: Literal[SimulationEventType.SPOILAGE] = SimulationEventType.SPOILAGE
    node_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)


class StockoutEvent(SimulationEvent):
    """Unmet store demand caused by unavailable inventory."""

    event_type: Literal[SimulationEventType.STOCKOUT] = SimulationEventType.STOCKOUT
    store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)
    unit_retail_price: float = Field(..., ge=0.0)


class MarkdownEvent(SimulationEvent):
    """Store inventory sold or offered at a reduced retail price."""

    event_type: Literal[SimulationEventType.MARKDOWN] = SimulationEventType.MARKDOWN
    store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    original_unit_retail_price: float = Field(..., ge=0.0)
    markdown_unit_retail_price: float = Field(..., ge=0.0)

    @model_validator(mode="after")
    def validate_markdown_price(self) -> Self:
        """Ensure a markdown does not increase the retail price."""
        if self.markdown_unit_retail_price > self.original_unit_retail_price:
            msg = "markdown_unit_retail_price must not exceed original_unit_retail_price"
            raise ValueError(msg)
        return self


class StoreTransferEvent(SimulationEvent):
    """Rare inventory movement between stores."""

    event_type: Literal[SimulationEventType.STORE_TRANSFER] = SimulationEventType.STORE_TRANSFER
    source_store_id: str = Field(..., min_length=3)
    target_store_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0.0)
    transfer_cost: float = Field(..., ge=0.0)

    @model_validator(mode="after")
    def validate_distinct_stores(self) -> Self:
        """Ensure a transfer moves inventory between different stores."""
        if self.source_store_id == self.target_store_id:
            msg = "source_store_id and target_store_id must be different"
            raise ValueError(msg)
        return self


class SupplierDelayEvent(SimulationEvent):
    """Supplier shipment delayed before warehouse receipt."""

    event_type: Literal[SimulationEventType.SUPPLIER_DELAY] = SimulationEventType.SUPPLIER_DELAY
    supplier_id: str = Field(..., min_length=3)
    warehouse_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    quantity_units: int = Field(..., gt=0)
    delay_days: int = Field(..., gt=0)


class SupplierShortShipmentEvent(SimulationEvent):
    """Supplier shipment received below its expected quantity."""

    event_type: Literal[SimulationEventType.SUPPLIER_SHORT_SHIPMENT] = (
        SimulationEventType.SUPPLIER_SHORT_SHIPMENT
    )
    supplier_id: str = Field(..., min_length=3)
    warehouse_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    expected_quantity_units: int = Field(..., gt=0)
    received_quantity_units: int = Field(..., ge=0)
    unit_cost: float = Field(..., ge=0.0)

    @model_validator(mode="after")
    def validate_received_quantity(self) -> Self:
        """Ensure a short shipment does not exceed its expected quantity."""
        if self.received_quantity_units > self.expected_quantity_units:
            msg = "received_quantity_units must not exceed expected_quantity_units"
            raise ValueError(msg)
        return self
