"""Core domain models for Itara Fresh Intelligence.

These models define the operating world before simulation, forecasting, and
agentic decisioning are implemented.
"""

from __future__ import annotations

from datetime import date, time
from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProductCategory(StrEnum):
    """Fresh grocery product categories used in the simulation."""

    PRODUCE = "produce"
    DAIRY = "dairy"
    MEAT = "meat"
    BAKERY = "bakery"
    DELI = "deli"
    SEAFOOD = "seafood"
    PREPARED_FOODS = "prepared_foods"
    FLORAL = "floral"


class StorageType(StrEnum):
    """Storage requirements for a SKU."""

    AMBIENT = "ambient"
    CHILLED = "chilled"
    FROZEN = "frozen"


class StoreFormat(StrEnum):
    """Physical store format."""

    FLAGSHIP = "flagship"
    LARGE_URBAN = "large_urban"
    MEDIUM_URBAN = "medium_urban"
    SUBURBAN = "suburban"
    COMPACT_NEIGHBOURHOOD = "compact_neighbourhood"


class NetworkNodeType(StrEnum):
    """Types of nodes shown in the network visualizer."""

    STORE = "store"
    WAREHOUSE = "warehouse"
    SUPPLIER = "supplier"


class RiskLevel(StrEnum):
    """Standardized risk levels for future snapshots and decision traces."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DecisionAction(StrEnum):
    """Actions the decision layer may recommend."""

    NO_ACTION = "no_action"
    WAREHOUSE_ALLOCATION = "warehouse_allocation"
    WAREHOUSE_TO_STORE_DELIVERY = "warehouse_to_store_delivery"
    STORE_TRANSFER = "store_transfer"
    MARKDOWN = "markdown"
    SUPPLIER_PROCUREMENT_REVIEW = "supplier_procurement_review"
    SUPPLIER_PURCHASE_ORDER = "supplier_purchase_order"
    HUMAN_ESCALATION = "human_escalation"


class Coordinates(BaseModel):
    """Latitude and longitude for stores, warehouses, and suppliers."""

    model_config = ConfigDict(frozen=True)

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class Store(BaseModel):
    """A retail store served by the Itara central warehouse."""

    model_config = ConfigDict(frozen=True)

    store_id: str = Field(..., min_length=3)
    store_name: str = Field(..., min_length=3)
    district: str = Field(..., min_length=2)
    coordinates: Coordinates
    store_format: StoreFormat
    store_persona: str = Field(..., min_length=3)
    footfall_index: float = Field(..., ge=0.0, le=2.0)
    price_sensitivity_index: float = Field(..., ge=0.0, le=2.0)
    prepared_foods_affinity: float = Field(..., ge=0.0, le=2.0)
    fresh_produce_affinity: float = Field(..., ge=0.0, le=2.0)
    markdown_response_index: float = Field(..., ge=0.0, le=2.0)
    cold_storage_capacity_units: int = Field(..., gt=0)
    receiving_window_start: time
    receiving_window_end: time
    nearest_store_ids: tuple[str, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def validate_receiving_window(self) -> Self:
        """Ensure each store has a valid daily receiving window."""
        if self.receiving_window_start >= self.receiving_window_end:
            msg = "receiving_window_start must be earlier than receiving_window_end"
            raise ValueError(msg)
        return self


class Warehouse(BaseModel):
    """Central distribution centre serving the store network."""

    model_config = ConfigDict(frozen=True)

    warehouse_id: str = Field(..., min_length=3)
    warehouse_name: str = Field(..., min_length=3)
    coordinates: Coordinates
    average_days_of_cover: int = Field(..., ge=1, le=30)
    morning_dispatch_time: time
    afternoon_dispatch_time: time
    emergency_dispatch_allowed: bool
    emergency_dispatch_fixed_cost: float = Field(..., ge=0.0)
    transfer_max_radius_km: float = Field(..., gt=0.0)
    transfer_fixed_cost: float = Field(..., ge=0.0)
    transfer_cost_per_km: float = Field(..., ge=0.0)
    category_capacity_units: dict[ProductCategory, int]

    @field_validator("category_capacity_units")
    @classmethod
    def validate_category_capacity_units(
        cls,
        category_capacity_units: dict[ProductCategory, int],
    ) -> dict[ProductCategory, int]:
        """Ensure warehouse capacity is positive for every configured category."""
        if not category_capacity_units:
            msg = "category_capacity_units must not be empty"
            raise ValueError(msg)

        invalid_categories = [
            category.value
            for category, capacity in category_capacity_units.items()
            if capacity <= 0
        ]
        if invalid_categories:
            msg = f"category capacities must be positive: {invalid_categories}"
            raise ValueError(msg)

        return category_capacity_units


class Supplier(BaseModel):
    """Supplier that ships bulk inventory to the central warehouse."""

    model_config = ConfigDict(frozen=True)

    supplier_id: str = Field(..., min_length=3)
    supplier_name: str = Field(..., min_length=3)
    supplier_warehouse_name: str = Field(..., min_length=3)
    coordinates: Coordinates
    categories_supplied: tuple[ProductCategory, ...]
    normal_lead_time_days: int = Field(..., ge=0, le=14)
    emergency_delivery_allowed: bool
    emergency_delivery_fee: float = Field(..., ge=0.0)
    reliability_score: float = Field(..., ge=0.0, le=1.0)
    minimum_order_value: float = Field(..., ge=0.0)
    normal_delivery_days: tuple[str, ...]

    @field_validator("categories_supplied")
    @classmethod
    def validate_categories_supplied(
        cls,
        categories_supplied: tuple[ProductCategory, ...],
    ) -> tuple[ProductCategory, ...]:
        """Ensure each supplier covers at least one category."""
        if not categories_supplied:
            msg = "supplier must supply at least one product category"
            raise ValueError(msg)
        return categories_supplied

    @field_validator("normal_delivery_days")
    @classmethod
    def validate_normal_delivery_days(
        cls, normal_delivery_days: tuple[str, ...]
    ) -> tuple[str, ...]:
        """Ensure delivery days are defined."""
        if not normal_delivery_days:
            msg = "supplier must have at least one normal delivery day"
            raise ValueError(msg)
        return normal_delivery_days


class SKU(BaseModel):
    """Perishable product sold through the Itara Fresh network."""

    model_config = ConfigDict(frozen=True)

    sku_id: str = Field(..., min_length=3)
    sku_name: str = Field(..., min_length=3)
    category: ProductCategory
    subcategory: str = Field(..., min_length=2)
    supplier_id: str = Field(..., min_length=3)
    unit_retail_price: float = Field(..., gt=0.0)
    unit_cost: float = Field(..., gt=0.0)
    gross_margin_pct: float = Field(..., ge=0.0, le=1.0)
    shelf_life_days: int = Field(..., ge=1, le=60)
    case_pack_size: int = Field(..., gt=0)
    warehouse_case_pack_units: int = Field(..., gt=0)
    minimum_display_units: int = Field(..., ge=0)
    spoilage_rate_coefficient: float = Field(..., ge=0.0, le=2.0)
    substitution_group: str = Field(..., min_length=2)
    storage_type: StorageType
    cold_chain_required: bool

    @model_validator(mode="after")
    def validate_margin_matches_price_and_cost(self) -> Self:
        """Validate margin is consistent with retail price and unit cost."""
        calculated_margin = (self.unit_retail_price - self.unit_cost) / self.unit_retail_price
        if abs(calculated_margin - self.gross_margin_pct) > 0.05:
            msg = (
                "gross_margin_pct is inconsistent with unit_retail_price "
                f"and unit_cost for {self.sku_id}"
            )
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_cold_chain_matches_storage(self) -> Self:
        """Ensure chilled and frozen products are marked as cold-chain required."""
        requires_cold_chain = self.storage_type in {
            StorageType.CHILLED,
            StorageType.FROZEN,
        }
        if requires_cold_chain and not self.cold_chain_required:
            msg = (
                f"{self.sku_id} uses {self.storage_type.value} storage "
                "but cold_chain_required=False"
            )
            raise ValueError(msg)
        return self


class InventoryBatch(BaseModel):
    """Inventory batch with expiry tracking."""

    model_config = ConfigDict(frozen=True)

    batch_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    node_id: str = Field(..., min_length=3)
    node_type: NetworkNodeType
    received_date: date
    expiry_date: date
    on_hand_units: int = Field(..., ge=0)
    reserved_units: int = Field(..., ge=0)
    quality_hold_units: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_batch_dates_and_units(self) -> Self:
        """Validate expiry date and available inventory assumptions."""
        if self.expiry_date < self.received_date:
            msg = "expiry_date must not be earlier than received_date"
            raise ValueError(msg)

        unavailable_units = self.reserved_units + self.quality_hold_units
        if unavailable_units > self.on_hand_units:
            msg = "reserved_units + quality_hold_units must not exceed on_hand_units"
            raise ValueError(msg)

        return self


class DistanceMatrixEntry(BaseModel):
    """Distance between two network nodes."""

    model_config = ConfigDict(frozen=True)

    origin_node_id: str = Field(..., min_length=3)
    destination_node_id: str = Field(..., min_length=3)
    straight_line_distance_km: float = Field(..., ge=0.0)
    estimated_road_distance_km: float | None = Field(default=None, ge=0.0)
    estimated_drive_minutes: float | None = Field(default=None, ge=0.0)

    @model_validator(mode="after")
    def validate_distinct_nodes(self) -> Self:
        """Ensure distance rows do not describe a node to itself."""
        if self.origin_node_id == self.destination_node_id:
            msg = "origin_node_id and destination_node_id must be different"
            raise ValueError(msg)
        return self


class MapNode(BaseModel):
    """Map-ready representation of a store, warehouse, or supplier."""

    model_config = ConfigDict(frozen=True)

    node_id: str = Field(..., min_length=3)
    node_type: NetworkNodeType
    node_name: str = Field(..., min_length=3)
    coordinates: Coordinates
    region: str | None = None
    category_coverage: tuple[ProductCategory, ...] = Field(default_factory=tuple)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DailyInventorySnapshot(BaseModel):
    """Daily inventory state used by simulation and the future map visualizer."""

    model_config = ConfigDict(frozen=True)

    snapshot_date: date
    node_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    on_hand_units: int = Field(..., ge=0)
    available_to_allocate_units: int = Field(..., ge=0)
    days_of_cover: float = Field(..., ge=0.0)
    stockout_risk: RiskLevel
    spoilage_risk: RiskLevel
    overstock_risk: RiskLevel

    @model_validator(mode="after")
    def validate_available_units(self) -> Self:
        """Ensure available units do not exceed on-hand units."""
        if self.available_to_allocate_units > self.on_hand_units:
            msg = "available_to_allocate_units must not exceed on_hand_units"
            raise ValueError(msg)
        return self


class AgentDecisionTrace(BaseModel):
    """Trace ledger entry for policy-grounded agent decisions.

    Most fields are optional in Phase 1 because the full agent is introduced later.
    The model exists now to preserve the long-term decision trace contract.
    """

    model_config = ConfigDict(frozen=True)

    trace_id: str = Field(..., min_length=3)
    decision_date: date
    node_id: str = Field(..., min_length=3)
    sku_id: str | None = None
    recommended_action: DecisionAction
    risk_level: RiskLevel | None = None
    expected_savings: float | None = Field(default=None, ge=0.0)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    policy_references: tuple[str, ...] = Field(default_factory=tuple)
    tool_calls: tuple[str, ...] = Field(default_factory=tuple)
    escalation_required: bool = False
    reason_codes: tuple[str, ...] = Field(default_factory=tuple)
