# Itara Fresh Intelligence Project State

Last updated: 2026-07-10

This is the living project state report for Itara Fresh Intelligence. It should
be treated as a practical handoff document for understanding what the
repository currently implements, what remains planned, and what should be built
next.

## Project mission

Itara Fresh Intelligence is an operations-first replenishment intelligence
system for a fresh grocery network.

The system is intended to answer:

> What fresh inventory should move where, when, why, and with what modeled
> financial impact?

The project is not a generic AI-agent demo. It is a business-loss reduction
system whose recommendations must be grounded in operational data,
deterministic logic, policy, logistics constraints, and modeled financial
outcomes.

## End goal

The intended end state is a replayable operating system for a simulated fresh
grocery network that can:

- define stores, warehouse, suppliers, SKUs, policy, logistics, and distances
- simulate operating history from 2022 through 2025
- calculate spoilage loss, stockout lost margin, markdown margin loss,
  transfer cost, holding cost, inference cost, and net loss
- forecast demand and detect operational risk
- allocate warehouse inventory before considering other actions
- use store-to-store transfers only as rare, policy-constrained exceptions
- trigger supplier procurement only for network-level shortages
- use RAG for unstructured policy and contract evidence
- use agentic reasoning only for action-required, policy-sensitive, uncertain,
  or high-exposure cases
- verify recommendations against inventory, freshness, logistics, policy, and
  financial constraints
- save explainable decision traces
- later add a contextual-bandit advisor and token-aware inference routing
- present the operating story through a map-based console and modeled business
  impact narrative

No real-world savings have been proven yet. Any future public savings or ROI
claim must come from simulation and financial calculations and must be labeled
as modeled unless validated in a real deployment.

## Current phase

The repository is in Phase 2: early simulator and financial-loss foundation.

Phase 1 is substantially complete. Phase 2 has started and now includes event
schemas, financial loss formulas, a bounded deterministic baseline day
simulator, generated SKU catalog integration for the baseline simulator, a
daily financial impact summarizer, daily inventory state contracts, and a
small event-to-inventory-state transition skeleton, a bounded baseline replay
runner, a frontend-readable static simulation summary artifact, and a baseline
smoke report.

The repository does not yet contain the full four-year simulator, a real
inventory state transition engine, demand forecasting, risk detection,
allocation logic, procurement logic, Qdrant indexing, agent orchestration, or
learned decision support.

## Completed Phase 1 work

Phase 1 established the static operating world and the visual shell.

Implemented backend foundation:

- Python package and quality tooling configured through `pyproject.toml`
- strict pytest, ruff, and mypy setup
- typed Pydantic domain models for stores, warehouse, suppliers, SKUs,
  inventory batches, map nodes, distance rows, daily inventory snapshots, and
  future decision traces
- static configuration for 15 Ontario stores
- static configuration for 1 central warehouse
- static configuration for 10 suppliers
- deterministic 500-SKU catalog generation with 40 named anchor SKUs
- policy Markdown documents for replenishment, transfer exceptions, supplier
  procurement, markdowns, and human escalation
- policy loading utilities for Markdown policy documents
- geospatial/network artifact foundation documented and validated by tests
- generated network artifacts consumed by the frontend
- Phase 1 validation command and tests

Implemented frontend foundation:

- Next.js app under `apps/web`
- TypeScript, Tailwind, and MapLibre-based network visualizer
- backend-generated network JSON consumed by the frontend
- map rendering for 15 stores, 10 suppliers, and 1 warehouse
- node search and node-type filters
- clickable markers and popups
- side-panel node selection and scrolling
- supplier-to-warehouse relationship overlay
- warehouse-to-store relationship overlay
- two static store-to-store transfer exception examples
- independent route toggles
- operational flow summary

Current visual routes are relationship and operating-flow overlays. They are
not optimized routes, dispatch schedules, allocation recommendations, or
policy-verified transfer decisions.

## Completed Phase 2 work

Implemented Phase 2 foundation:

- stable simulator event types
- immutable Pydantic event contracts for sales, warehouse receipts, warehouse
  allocations, store deliveries, inventory counts, spoilage, stockouts,
  markdowns, store transfers, supplier delays, and supplier short shipments
- validation for positive quantities, non-negative financial values, markdown
  price constraints, distinct transfer stores, and short-shipment quantities
- pure financial formulas for spoilage loss, stockout lost margin, markdown
  margin loss, transfer cost, holding cost, and net loss
- immutable `FinancialImpactSummary` contract that validates net loss equals
  the sum of its components
- small deterministic baseline day simulator
- generated SKU catalog loader for simulation use
- baseline simulator SKU selection from the generated 500-SKU catalog
- event type summarizer
- daily financial impact summarizer for supported loss event types
- daily inventory state contracts for positions, store state, warehouse state,
  and network state
- small transition skeleton for applying selected events to daily inventory
  state
- bounded baseline replay runner that applies replay-safe event transitions
  across multiple days and returns daily inventory and financial summaries
- JSON exporter for a small frontend-readable baseline simulation summary
- bounded multi-day baseline smoke report
- tests for simulator events, financial formulas, baseline simulation, daily
  impact aggregation, inventory replay, frontend summary export, and smoke
  report output

## Current backend modules

`src/itara/domain/`

- Defines the core domain contracts and enums.
- Includes stores, warehouse, suppliers, SKUs, inventory batches, map nodes,
  daily inventory snapshots, and future agent decision traces.
- Includes deterministic SKU catalog generation.
- Does not execute simulation, forecasting, allocation, procurement, or agent
  decisions.

`src/itara/sim/`

- Defines simulator event contracts in `events.py`.
- Defines pure financial formulas and `FinancialImpactSummary` in
  `financials.py`.
- Provides a small deterministic baseline event stream in `baseline.py`.
- Loads the generated SKU catalog and uses a deterministic two-SKU slice for
  the current baseline smoke simulation.
- Aggregates supported event types into daily modeled financial impact in
  `impact.py`.
- Defines daily inventory state contracts in `state.py`.
- Applies a small supported set of events to daily inventory state in
  `transitions.py`.
- Runs a bounded multi-day baseline inventory replay in `replay.py`.
- Produces a bounded Markdown smoke report and a static frontend simulation
  summary JSON artifact in `reports.py`.
- Does not yet apply all event types to inventory state, generate full
  operating streams, run a four-year replay, or compare baseline versus
  intervention.

`src/itara/rag/`

- Loads Markdown policy documents from `data/policies`.
- Extracts policy IDs, titles, content, paths, and word counts.
- Provides lookup by policy ID.
- Does not yet chunk, embed, index, retrieve, or use Qdrant.

`data/config/`

- Stores the static operating configuration for stores, suppliers, and the
  warehouse.
- Includes receiving windows, store personas, supplier lead times, delivery
  days, reliability assumptions, emergency delivery fields, warehouse dispatch
  settings, category capacity, and transfer cost assumptions.

`data/generated/sku_catalog.json`

- Stores the generated 500-SKU catalog artifact used by the current baseline
  simulator.
- Gives simulator events catalog-backed SKU IDs, unit costs, retail prices, and
  margins instead of disconnected sample values.

`data/policies/`

- Contains the current retrieval-ready policy Markdown source documents:
  replenishment, store transfer exception, supplier procurement, markdown, and
  human escalation.
- These are source policy documents only. They are not yet indexed into a
  vector database.

## Current frontend features

The frontend currently provides a static operating-world visualizer.

Implemented:

- network map using MapLibre
- OpenStreetMap raster tile base map
- colored markers for warehouse, stores, and suppliers
- marker popups with node type, name, region, coordinates, categories, and ID
- selected-node fly-to behavior
- search across node ID, name, type, region, and category coverage
- filters for all nodes, warehouse, stores, and suppliers
- side-panel cards grouped by warehouse, stores, and suppliers
- visible counts for filtered nodes
- route overlays for supplier inbound routes, warehouse outbound routes, and
  static transfer exception examples
- independent toggles for each route overlay
- metric cards for network summary values
- compact baseline simulation smoke summary rendered from static JSON

Not implemented in the frontend:

- date-driven network replay
- SKU-level inventory state
- simulated daily events on the map
- financial loss map overlays or charts
- forecast or risk overlays
- generated allocation recommendations
- policy-verified transfer recommendations
- supplier procurement warnings
- agent tool calls, policy citations, or decision traces
- API-backed live state

## Current simulator capability

The simulator can currently generate a small deterministic baseline event stream
for one simulated day through `simulate_baseline_day`.

Current scope:

- fixed stores: `store_001` and `store_004`
- deterministic SKU slice loaded from the generated 500-SKU catalog:
  `sku_0001` and `sku_0002`
- fixed warehouse: `warehouse_001`
- deterministic random values when a seed is provided
- stable event IDs derived from simulation date and sequence
- catalog-backed unit cost and unit retail price values for sale, stockout,
  spoilage, and markdown events where those fields apply
- generated event types: sales, one stockout, one spoilage event, one markdown,
  and inventory counts for the two stores and the warehouse
- deterministic event count by type for the default day:
  - `sale`: 4
  - `stockout`: 1
  - `spoilage`: 1
  - `markdown`: 1
  - `inventory_count`: 6

This is a smoke-test simulator foundation. It is not the full operations
simulator and does not yet model real inventory movement, expiry by batch,
warehouse receipts, allocation state, delivery execution, supplier variability,
or four-year replay.

Catalog integration matters because simulated losses now use product values
from the same generated SKU artifact that represents the operating world. This
keeps the smoke simulation small while removing disconnected hardcoded sample
prices and costs. It does not make the current losses realistic yet; realism
still depends on broader event generation, inventory state transitions, demand
patterns, and invariant checks.

## Current inventory state capability

The simulator now has daily inventory state contracts in `src/itara/sim/state.py`.

Implemented state contracts:

- `InventoryPosition`: one SKU at one node on one simulation date
- `StoreDailyInventoryState`: all tracked inventory positions for one store on
  one date
- `WarehouseDailyInventoryState`: all tracked inventory positions for one
  warehouse on one date
- `NetworkDailyInventoryState`: one warehouse state plus store states for one
  network date

The contracts support:

- required state date
- store, warehouse, or node identity
- SKU identity
- on-hand units
- reserved units
- available units
- expired units
- near-expiry units
- unit cost
- unit retail price
- optional days of cover

Validation currently enforces non-negative units and financial values,
non-negative days of cover when present, available units not exceeding on-hand
units, and date/node consistency inside store, warehouse, and network daily
state objects.

The state contracts include aggregate helpers for total on-hand units, total
available units, and total expired units.

## Current transition capability

The simulator now has a small transition skeleton in
`src/itara/sim/transitions.py`.

Implemented transition functions:

- `apply_event_to_state(state, event)`
- `apply_events_to_state(initial_state, events)`

Supported event transitions:

- `SaleEvent`: reduces store `on_hand_units` and `available_units`
- `SpoilageEvent`: reduces `on_hand_units` and `available_units`, and
  increases `expired_units`
- `InventoryCountEvent`: sets observed `on_hand_units` and clamps
  `available_units` so it does not exceed on-hand inventory
- `WarehouseReceiptEvent`: increases warehouse `on_hand_units` and
  `available_units`
- `StoreDeliveryEvent`: reduces warehouse `on_hand_units` and
  `available_units`, then increases target store `on_hand_units` and
  `available_units`

When a warehouse receipt or store delivery references a SKU position that does
not exist yet, the transition layer creates a new position. Receipt and
delivery event schemas currently carry unit cost but not retail price, so newly
created positions use `unit_retail_price=0.0` until those events are enriched
or the transition layer receives catalog-price context.

Current invariant checks:

- event date must match state date
- transitions must not make `on_hand_units` negative
- transitions must not make `available_units` negative
- store delivery must not make warehouse inventory negative
- resulting state is revalidated through the inventory state contracts, which
  enforce `available_units <= on_hand_units`

Unsupported event transitions currently raise `NotImplementedError` by design
so missing semantics remain visible. Unsupported events include:

- `WarehouseAllocationEvent`
- `MarkdownEvent`
- `StoreTransferEvent`
- `SupplierDelayEvent`
- `SupplierShortShipmentEvent`

This is not a full state transition engine yet. It proves that the event
stream can update daily inventory state for a small tested subset, including
basic warehouse inbound and warehouse-to-store movement, before the project
expands to allocations, markdowns, transfers, procurement, and generated
multi-day replay.

State is required before realistic simulation, forecasting, decisions, and RL
because events alone only describe what happened. The system also needs a
validated picture of what inventory exists after events before it can forecast
from inventory history, detect stockout or spoilage risk, allocate warehouse
inventory, verify transfer eligibility, trigger network procurement, calculate
credible modeled losses, or train a contextual-bandit advisor without bypassing
deterministic constraints.

## Current replay capability

The simulator now has a bounded baseline replay runner in
`src/itara/sim/replay.py`.

Implemented replay contracts and function:

- `DailyReplayResult`
- `BaselineReplayResult`
- `run_baseline_replay(start_date, days=7, seed=42)`

The replay runner currently:

- creates deterministic initial inventory state for the baseline stores,
  warehouse, and catalog-backed baseline SKUs
- advances daily inventory state dates while carrying quantities forward
- runs `simulate_baseline_day` for each simulated day
- applies replay-safe inventory transitions for physical inventory movement
  events currently represented in the baseline stream
- records skipped state-event counts for events that are not yet replay-safe
  for inventory mutation
- summarizes daily modeled financial impact with
  `summarize_daily_financial_impact`
- returns daily event counts, daily financial impact, daily ending inventory
  state, and final network inventory state

Current replay limitations:

- the replay is bounded and intended for smoke-level simulator foundation work
- baseline inventory count events are recorded but not applied as authoritative
  reconciliation in replay yet, because the current baseline generator is not
  state-aware and random counts can otherwise make later generated sales
  impossible
- stockout and markdown events still affect financial summaries but do not yet
  mutate inventory state
- warehouse receipt and store delivery transitions are implemented, but the
  current baseline generator does not yet emit those events
- this is not a full four-year simulator, generated operating dataset, or
  baseline-versus-intervention comparison

## Current backend-to-frontend simulation artifact

The backend can now export a small static JSON summary for the Next.js app with
`write_frontend_simulation_summary`.

Current artifact:

- path: `apps/web/src/data/simulation-summary.json`
- source: `run_baseline_replay(date(2022, 1, 3), days=7, seed=42)`
- TypeScript loader: `apps/web/src/data/simulation.ts`
- UI component: `apps/web/src/components/baseline-simulation-summary.tsx`

The JSON includes:

- simulation start and end dates
- simulated day count
- total event count
- event counts by type
- total spoilage loss
- total stockout lost margin
- total markdown margin loss
- total transfer cost
- total holding cost
- total inference cost
- total modeled net loss
- daily modeled net loss values

The UI now shows a compact section titled "Baseline simulation smoke summary"
above the network visualizer. It displays simulated days, total events,
modeled net loss, and the top event counts, with an explicit label that this is
a smoke simulation and not a savings claim.

This is a deployment-minded static artifact path. FastAPI is still planned for
later; it has not been built yet.

## Current financial calculation capability

The financial layer can calculate:

- spoilage loss as expired units multiplied by unit cost
- stockout lost margin as unmet demand units multiplied by retail price and
  gross margin percentage
- markdown margin loss as markdown units multiplied by margin reduction per
  unit
- transfer cost as fixed handling cost plus distance cost
- holding cost as excess inventory units multiplied by unit cost and daily
  holding rate
- net loss as the sum of spoilage loss, stockout lost margin, markdown margin
  loss, transfer cost, holding cost, and inference cost

The formulas validate that inputs are finite and non-negative. Stockout gross
margin percentage must not exceed 1. `FinancialImpactSummary` rejects summaries
where `net_loss` does not equal the sum of all components.

Daily impact aggregation currently summarizes spoilage, stockout, markdown, and
store-transfer events. Holding cost and inference cost are present in the
summary contract but are currently set to zero by the daily event summarizer.

## Current smoke report capability

The repository can produce a small deterministic Markdown smoke report through
`run_baseline_smoke_report`.

The report currently includes:

- report title
- explicit statement that the result is a smoke test, not optimized operations
  or savings
- simulation start date
- simulation end date
- simulated day count
- initial seed
- total event count
- event count by type
- total spoilage loss
- total stockout lost margin
- total markdown margin loss
- total transfer cost
- total holding cost
- total inference cost
- total modeled net loss

For the tested seven-day smoke window starting 2022-01-03 with seed 42, tests
expect 91 total events.

This report is useful as a wiring check. It is not an annual loss report, a
baseline-versus-intervention report, or evidence of savings.

## What is not built yet

The following are planned but not implemented:

- full deterministic event generator across the network
- full daily inventory state transition engine
- batch-level freshness and expiry transitions
- warehouse receipt generation from supplier schedules
- warehouse allocation transitions
- generated store delivery events in baseline flows
- supplier delay and short-shipment generation in baseline flows
- generated multi-day operating datasets beyond the bounded smoke and replay
  path
- four-year 2022-2025 replay
- annual baseline loss reports
- counterfactual baseline-versus-intervention reports
- API-backed simulation summary endpoints
- demand forecasting
- forecasting training tables
- risk detection
- deterministic warehouse-first allocation engine
- transfer eligibility engine
- network-level supplier procurement engine
- transfer-rate guardrail evaluation
- FastAPI endpoints
- Qdrant indexing and retrieval
- policy-grounded agent workflow
- decision trace persistence beyond the domain contract
- contextual bandit or other learned advisor
- token-aware inference routing
- deployment stack
- production observability
- public demo narrative backed by modeled results

## Where RL/contextual bandit fits later

The first learned advisor should be a contextual bandit, not PPO or CQL.

It belongs after:

1. simulator contracts are stable
2. inventory state transitions are implemented
3. financial impact calculations are credible
4. baseline-versus-intervention comparisons exist
5. forecasting and risk detection are working
6. deterministic warehouse allocation, transfer eligibility, and procurement
   checks are implemented
7. policy and logistics verification are enforced

The learned advisor should return a structured recommendation or ranking. It
must not bypass deterministic verification, policy checks, freshness checks,
logistics constraints, financial simulation, or human escalation rules. PPO and
CQL remain optional research extensions, not launch requirements.

## Next recommended milestones

Recommended near-term sequence:

1. Make the baseline generator state-aware enough to emit warehouse receipts
   and store deliveries before daily demand consumes inventory.
2. Add a repeatable artifact-generation workflow for frontend-facing simulator
   JSON as more summary fields are added.
3. Apply inventory count reconciliation semantics once the generator can keep
   replay state feasible across days.
4. Extend transition support to warehouse allocation, markdown, transfer,
   supplier delay, and supplier short-shipment events.
5. Add invariant checks for event consistency, conservation of units, and
   freshness constraints.
6. Expand the baseline generator from the tiny smoke sample to a bounded
   multi-store, multi-SKU window.
7. Generate warehouse receipt, allocation, store delivery, supplier delay, and
   supplier short-shipment events in controlled baseline flows.
8. Aggregate daily financial impact from generated event streams.
9. Write bounded baseline reports from generated simulation output.
10. Add realism checks before scaling toward four years.
11. Build forecasting tables and simple baseline forecasts.
12. Add risk detection.
13. Build warehouse-first allocation logic.
14. Add transfer eligibility and network procurement logic.
15. Introduce API, RAG, and agent tooling only after the deterministic
    simulator and decision baseline are tested.

Do not create huge generated datasets yet. Keep samples small and deterministic
until contracts, transitions, and invariants are stable.

## Latest known repo state

This section was generated from the repository before this report was committed.

Latest `git log --oneline -10`:

```text
bd78baf Add baseline inventory replay runner
89b8800 Support warehouse receipt and store delivery transitions
be3af1a Add inventory state transition skeleton
529beda Add daily inventory state contracts
bf42e02 Connect baseline simulator to SKU catalog
0ebc2a8 Add living project state report
6033e7c Add baseline simulation smoke report
c7eed49 Summarize daily financial impact from events
05be30b Add baseline daily simulator skeleton
e16f6bb Restore project operating guide
```

Latest pytest result observed while preparing this report:

```text
133 passed
```

Latest frontend checks observed while preparing this report:

```text
npm run lint: passed
npm run build: passed
```

Latest Phase 1 validation summary:

```json
{
  "distance_matrix_entry_count": 650,
  "network_node_count": 26,
  "passed": true,
  "policy_document_count": 5,
  "product_category_count": 8,
  "sku_count": 500,
  "store_count": 15,
  "supplier_count": 10,
  "warehouse_count": 1
}
```

## How to test current state

Run backend checks from the repository root:

```powershell
ruff format src tests
ruff check src tests
mypy src
pytest -q
```

Run Phase 1 validation from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -c "from itara.validation import main; main()"
```

Run frontend checks from `apps/web`:

```powershell
cd apps/web
npm run lint
npm run build
cd ../..
```

Print the current baseline smoke report from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -c "from datetime import date; from itara.sim import run_baseline_smoke_report; print(run_baseline_smoke_report(date(2022, 1, 3), days=7, seed=42))"
```

Regenerate the frontend simulation summary JSON from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -c "from datetime import date; from pathlib import Path; from itara.sim import write_frontend_simulation_summary; write_frontend_simulation_summary(Path('apps/web/src/data/simulation-summary.json'), date(2022, 1, 3), days=7, seed=42)"
```

## Update rule

This file must be updated after every successful implementation prompt.

When the repository gains a meaningful implemented capability, update this
report in the same change or in the next focused documentation change. Keep it
honest: clearly separate implemented behavior from scaffolding and future
plans, and do not claim savings until they come from simulation and financial
calculations.
