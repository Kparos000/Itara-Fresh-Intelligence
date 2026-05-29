# Itara Fresh Intelligence — Domain Model

This document defines the first production-grade domain model for Itara Fresh Intelligence.

The domain model exists before the simulator, forecasting layer, RAG layer, and agentic workflow because every later system depends on a stable representation of the operating world.

---

## Domain design principles

1. The project is operations-first.
2. Suppliers deliver to the warehouse, not directly to stores by default.
3. Store replenishment starts with warehouse inventory.
4. Supplier procurement is network-level.
5. Store-to-store transfer is an exception.
6. Forecasting predicts risk; it does not decide actions alone.
7. Agent decisions must produce traceable decision records.
8. The map visualizer must use the same core location and state contracts as the backend.

---

## Core entities

### Store

A retail location served by the central warehouse.

Important fields:

- store ID
- store name
- district
- coordinates
- format
- persona
- footfall index
- price sensitivity
- category affinities
- markdown response index
- cold storage capacity
- receiving window
- nearest store IDs

### Warehouse

The central distribution centre that receives supplier deliveries and serves stores.

Important fields:

- warehouse ID
- warehouse name
- coordinates
- days of cover
- dispatch windows
- emergency dispatch settings
- transfer cost settings
- category-level capacity

### Supplier

A supplier ships bulk inventory to the warehouse.

Important fields:

- supplier ID
- supplier name
- supplier warehouse name
- coordinates
- categories supplied
- lead time
- emergency delivery rules
- reliability score
- minimum order value
- delivery days

### SKU

A perishable product sold through the network.

Important fields:

- SKU ID
- SKU name
- category
- supplier ID
- retail price
- unit cost
- margin
- shelf life
- case pack size
- minimum display units
- spoilage coefficient
- substitution group
- storage type
- cold-chain requirement

### InventoryBatch

A batch of inventory at a store, warehouse, or supplier-facing location.

Important fields:

- batch ID
- SKU ID
- node ID
- node type
- received date
- expiry date
- on-hand units
- reserved units
- quality-hold units

### DistanceMatrixEntry

A reusable distance row between two network nodes.

The distance matrix should be generated once and reused by simulation and operations logic.

### MapNode

A map-ready representation of a store, warehouse, or supplier.

This lets the frontend visualizer start with the same location contract used by backend systems.

### DailyInventorySnapshot

A date-specific inventory state used by the simulator and map visualizer.

### AgentDecisionTrace

A trace ledger record for future agent decisions.

This model exists in Phase 1 so the project preserves the shape of future auditable agent decisions even before the agent is implemented.

---

## Validation rules

Current validation includes:

- latitude must be between -90 and 90
- longitude must be between -180 and 180
- receiving window start must be earlier than receiving window end
- warehouse category capacities must be positive
- supplier must supply at least one category
- supplier must have at least one delivery day
- SKU retail price and cost must imply a margin close to the declared margin
- chilled or frozen SKUs must require cold chain
- inventory expiry date must not be earlier than received date
- reserved plus quality-hold inventory must not exceed on-hand inventory
- available inventory must not exceed on-hand inventory
- distance matrix rows cannot describe a node to itself

---

## Relationship to future phases

Phase 1:

- defines static entities and contracts

Phase 2:

- generates events and daily inventory snapshots

Phase 3:

- attaches forecasts and risk scores

Phase 4:

- uses warehouse, transfer, supplier, and distance contracts for deterministic decisions

Phase 5:

- writes `AgentDecisionTrace` records after policy-grounded decisions

Phase 6:

- adds learned advisor recommendations and token-aware routing

Phase 7:

- evaluates schema validity, decision quality, policy compliance, and observability

Phase 8:

- exposes the full system through the interactive demo
