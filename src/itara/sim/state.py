"""Daily inventory state contracts for the Phase 2 simulator."""

from __future__ import annotations

from datetime import date
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InventoryPosition(BaseModel):
    """Inventory state for one SKU at one network node on one simulation date."""

    model_config = ConfigDict(frozen=True)

    state_date: date
    node_id: str = Field(..., min_length=3)
    sku_id: str = Field(..., min_length=3)
    on_hand_units: int = Field(..., ge=0)
    reserved_units: int = Field(..., ge=0)
    available_units: int = Field(..., ge=0)
    expired_units: int = Field(..., ge=0)
    near_expiry_units: int = Field(..., ge=0)
    unit_cost: float = Field(..., ge=0.0)
    unit_retail_price: float = Field(..., ge=0.0)
    days_of_cover: float | None = Field(default=None, ge=0.0)

    @model_validator(mode="after")
    def validate_available_units(self) -> Self:
        """Ensure allocatable inventory does not exceed physical inventory."""
        if self.available_units > self.on_hand_units:
            msg = "available_units must not exceed on_hand_units"
            raise ValueError(msg)
        return self


class StoreDailyInventoryState(BaseModel):
    """All tracked SKU inventory positions for one store on one date."""

    model_config = ConfigDict(frozen=True)

    state_date: date
    store_id: str = Field(..., min_length=3)
    positions: tuple[InventoryPosition, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def validate_positions_match_store_and_date(self) -> Self:
        """Ensure store state only contains same-date positions for that store."""
        for position in self.positions:
            if position.state_date != self.state_date:
                msg = "position state_date must match store state_date"
                raise ValueError(msg)
            if position.node_id != self.store_id:
                msg = "position node_id must match store_id"
                raise ValueError(msg)
        return self

    def total_on_hand_units(self) -> int:
        """Return total on-hand inventory units across all positions."""
        return sum(position.on_hand_units for position in self.positions)

    def total_available_units(self) -> int:
        """Return total available inventory units across all positions."""
        return sum(position.available_units for position in self.positions)

    def total_expired_units(self) -> int:
        """Return total expired inventory units across all positions."""
        return sum(position.expired_units for position in self.positions)


class WarehouseDailyInventoryState(BaseModel):
    """All tracked SKU inventory positions for one warehouse on one date."""

    model_config = ConfigDict(frozen=True)

    state_date: date
    warehouse_id: str = Field(..., min_length=3)
    positions: tuple[InventoryPosition, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def validate_positions_match_warehouse_and_date(self) -> Self:
        """Ensure warehouse state only contains same-date positions for that warehouse."""
        for position in self.positions:
            if position.state_date != self.state_date:
                msg = "position state_date must match warehouse state_date"
                raise ValueError(msg)
            if position.node_id != self.warehouse_id:
                msg = "position node_id must match warehouse_id"
                raise ValueError(msg)
        return self

    def total_on_hand_units(self) -> int:
        """Return total on-hand inventory units across all positions."""
        return sum(position.on_hand_units for position in self.positions)

    def total_available_units(self) -> int:
        """Return total available inventory units across all positions."""
        return sum(position.available_units for position in self.positions)

    def total_expired_units(self) -> int:
        """Return total expired inventory units across all positions."""
        return sum(position.expired_units for position in self.positions)


class NetworkDailyInventoryState(BaseModel):
    """Store and warehouse inventory state for one simulated network date."""

    model_config = ConfigDict(frozen=True)

    state_date: date
    warehouse_state: WarehouseDailyInventoryState
    store_states: tuple[StoreDailyInventoryState, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def validate_states_match_network_date(self) -> Self:
        """Ensure all included state snapshots share the network state date."""
        if self.warehouse_state.state_date != self.state_date:
            msg = "warehouse_state state_date must match network state_date"
            raise ValueError(msg)

        for store_state in self.store_states:
            if store_state.state_date != self.state_date:
                msg = "store_state state_date must match network state_date"
                raise ValueError(msg)
        return self

    def total_on_hand_units(self) -> int:
        """Return total on-hand inventory units across stores and warehouse."""
        return self.warehouse_state.total_on_hand_units() + sum(
            store_state.total_on_hand_units() for store_state in self.store_states
        )

    def total_available_units(self) -> int:
        """Return total available inventory units across stores and warehouse."""
        return self.warehouse_state.total_available_units() + sum(
            store_state.total_available_units() for store_state in self.store_states
        )

    def total_expired_units(self) -> int:
        """Return total expired inventory units across stores and warehouse."""
        return self.warehouse_state.total_expired_units() + sum(
            store_state.total_expired_units() for store_state in self.store_states
        )
