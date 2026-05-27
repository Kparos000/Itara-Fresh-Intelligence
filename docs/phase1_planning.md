\# Itara Fresh Intelligence — Phase 1 Planning Decisions and Network Simulation Visualizer Plan



Author: Kparobor Akpomiemie  

Project: Itara Fresh Intelligence  

Repository: https://github.com/Kparos000/Itara-Fresh-Intelligence  

Planning document version: 0.1  

Date: 2026-05-27



\---



\## 1. Planning position



The project is being planned as an operations-first decision-intelligence system, not a generic AI-agent demo.



The warehouse-first operating model remains the spine of the project:



\- suppliers deliver to the central distribution centre

\- stores are served from the warehouse first

\- store-to-store transfers are rare exceptions

\- supplier procurement is triggered only when the whole network is short



The map-based network simulation visualizer is now part of Phase 1. It should start as a static/mock visual operating model and later connect to simulation outputs, forecasts, risk signals, decisions, and financial impact.



Correct interpretation:



\- Phase 1 defines the world.

\- Phase 1 also creates a visual shell of that world.

\- Phase 2 creates time-based operational state.

\- Phase 3 adds forecasts and risk.

\- Phase 4 adds deterministic decision logic.

\- Phase 5 adds the policy-grounded agent.

\- Phase 6 adds learned decision advice and token-aware routing.

\- Phase 7 proves the system with evals and observability.

\- Phase 8 packages the full demo and launch story.



\---



\## 2. Recommended technology decision for the network visualizer



Recommended default stack:



\- Frontend framework: Next.js with TypeScript

\- UI layer: Tailwind CSS and shadcn/ui

\- Map engine: MapLibre GL JS

\- Data visualization layer: deck.gl where needed

\- Geospatial utilities: Turf.js

\- Backend API: FastAPI

\- Static geospatial format: GeoJSON

\- Operational data format: Parquet for generated simulation outputs, PostgreSQL later for API-backed queries

\- Map tiles: start with free/open tile styles for development; optionally switch to Mapbox later for a polished public demo



MapLibre GL JS should be the default because it gives a modern vector-map experience without locking the project into a proprietary map renderer.



deck.gl should be used later for richer visualizations such as:



\- inventory heatmaps

\- warehouse allocation flow arcs

\- transfer route arcs

\- animated supplier-to-warehouse inbound flows

\- store risk intensity layers



Turf.js should be used for lightweight geospatial calculations such as distances, GeoJSON utilities, and spatial filtering.



For Phase 1, distances can be calculated using Haversine. For later realism, the project may add OSRM or Mapbox Directions/Matrix API.



\---



\## 3. Revised Phase 1 scope



Phase 1 has two tracks.



\### Track A — Backend operational foundation



This includes:



\- repo scaffold

\- Python package structure

\- CI/CD

\- Pydantic schemas

\- YAML configs

\- domain model

\- store, warehouse, supplier, SKU definitions

\- relationship tests

\- logistics parameters

\- distance matrix generation

\- policy document skeletons



\### Track B — Network visualizer skeleton



This includes:



\- Next.js app skeleton under `apps/web`

\- map page showing 15 stores, warehouse, and supplier locations

\- date selector placeholder

\- entity side panel

\- store detail drawer placeholder

\- warehouse detail drawer placeholder

\- supplier detail drawer placeholder

\- API contract for location data

\- mock JSON data shaped like future API responses



The frontend should not require real inventory simulation yet. It should use typed mock state shaped exactly like the future API response.



\---



\## 4. Store network decision



Use the 15-store Ontario network, distributed across seven districts.



| District | Store count | Planning role |

|---|---:|---|

| Old Toronto | 3 | High-density, high-turnover, complex demand |

| North York | 2 | Suburban/transit hub demand, close to warehouse corridor |

| Scarborough | 2 | Longer-distance delivery pressure and isolated transfer cases |

| Mississauga | 2 | Large suburban demand, western logistics pressure |

| Etobicoke | 2 | Mid-distance from warehouse and useful transfer candidate zone |

| York | 2 | Price-sensitive and markdown-sensitive demand patterns |

| East York | 2 | Residential family demand and seasonal produce patterns |



Use distinct store formats from day one:



\- flagship

\- large urban

\- medium urban

\- suburban

\- compact neighbourhood



Each format should affect:



\- SKU assortment coverage

\- cold storage capacity

\- footfall index

\- average basket pattern

\- delivery receiving capacity

\- minimum display units

\- prepared-food demand

\- markdown sensitivity



Add `store\_persona` as a field separate from `store\_format`.



Recommended store behavior fields:



```text

store\_format

store\_persona

footfall\_index

price\_sensitivity\_index

prepared\_foods\_affinity

fresh\_produce\_affinity

markdown\_response\_index

cold\_storage\_capacity\_units

receiving\_window\_start

receiving\_window\_end

5\. Warehouse / distribution centre decision



Use one central warehouse/DC located around Weston/Finch or the Etobicoke/North York logistics corridor.



Planning assumptions:



12 average days of network inventory capacity

cold storage is the binding constraint

morning dispatch at 06:00

afternoon dispatch at 13:00

emergency dispatch allowed as rare exception with cost penalty

warehouse inventory has spoilage risk



Warehouse inventory should track:



on\_hand\_units

reserved\_units

quality\_hold\_units

near\_expiry\_units

available\_to\_allocate\_units

inbound\_units

expiry\_date

batch\_id



Without warehouse spoilage risk, the simulator would overstate the benefit of holding too much central inventory.



6\. Supplier decision



Use approximately 10 suppliers across 8 categories.



Category	Supplier count	Reason

Produce	2	Short shelf life, weather and seasonal volatility

Dairy	1	Stable contract, strict cold chain

Meat	2	Quality, lead-time, and refrigerated transport variability

Bakery	1	Near-daily replenishment

Deli	1	Contractually distinct from meat

Seafood	1	High spoilage risk and restricted delivery windows

Prepared foods	1	Internal or semi-internal kitchen supplier

Floral	1	Seasonal spikes and limited substitution



Emergency orders should be allowed for selected suppliers only.



Supplier reliability should be seasonal.



Substitution groups should be supported, but substitution behavior should vary by category.



Supplier data should include both operational and geospatial fields:



supplier\_latitude

supplier\_longitude

supplier\_warehouse\_name

normal\_delivery\_days

emergency\_delivery\_allowed



Structured supplier data should answer deterministic questions like lead time, MOQ, delivery days, and emergency fee. RAG documents should answer nuanced contract exceptions.



7\. SKU catalog decision



Use 500 perishable SKUs distributed across 8 categories.



Category	SKU count	Avg shelf life	Avg gross margin

Produce	120	4–7 days	35–40%

Dairy	80	14–21 days	25–30%

Meat	70	3–5 days	28–33%

Bakery	60	2–4 days	40–45%

Deli	50	7–14 days	30–35%

Seafood	40	2–3 days	32–38%

Prepared foods	50	1–3 days	42–48%

Floral	30	5–7 days	50–60%



Use a hybrid generation strategy:



40 named anchor SKUs for demo quality

460 generated SKUs from category templates



Required SKU fields:



sku\_id

sku\_name

category

subcategory

supplier\_id

unit\_retail\_price

unit\_cost

gross\_margin\_pct

shelf\_life\_days

case\_pack\_size

warehouse\_case\_pack\_units

minimum\_display\_units

spoilage\_rate\_coefficient

substitution\_group

storage\_type

cold\_chain\_required



Every SKU should have case-pack constraints. This is necessary for MOQ, warehouse allocation, and procurement realism.



Minimum display units should exist because a store can appear commercially out of stock before inventory reaches zero.



8\. Four-year timeline decision



Use the four-year timeline:



2022: baseline operations

2023: baseline operations

2024: AI intervention starts

2025: AI intervention matures



Use a 2024 soft launch:



January to March 2024: observe, recommend, and escalate only

April to December 2024: controlled execution with policy verification

2025: mature execution with learned advisor and token-aware routing



Baseline operations should include:



late markdowns

over-ordering before demand falls

under-ordering before holidays

weak supplier calendar awareness

inconsistent warehouse allocation

ad hoc transfers without strict profitability checks

no token-aware AI routing



A counterfactual replay should later replay 2023 demand conditions using the AI policy. This prevents weak claims where 2025 looks better simply because demand was easier.



9\. Phase 1 subphase decisions

Phase 1.1 — Domain model



Define the full entity relationship model before writing heavy logic.



Entities should include:



Store

Warehouse

Supplier

SKU

Category

InventoryBatch

SupplierPurchaseOrder

WarehouseAllocation

WarehouseToStoreDelivery

StoreTransfer

MarkdownEvent

SpoilageEvent

StockoutEvent

AgentDecisionTrace

MapNode

DistanceMatrixEntry

DailyInventorySnapshot



AgentDecisionTrace should be a typed Pydantic model from day one, but most fields can remain optional until Phase 5.



Phase 1.2 — Location and logistics model



Use realistic neighbourhood-centred coordinates for the 15 stores, warehouse, and supplier warehouses.



Generate:



data/generated/network\_nodes.geojson

data/generated/distance\_matrix.csv

Phase 1.3 — Supplier model



Supplier data should include operational fields and geospatial fields.



Phase 1.4 — Product and price model



Use category templates and seeded generation.



Phase 1.5 — Policy documents



Write policy documents after major parameters are fixed. Policy documents must match simulation constants exactly.



Phase 1.6 — Interactive network visualizer skeleton



Deliverables:



apps/web/

apps/web/app/network/page.tsx

apps/web/components/network-map.tsx

apps/web/components/entity-detail-panel.tsx

apps/web/components/date-selector.tsx

apps/web/lib/types.ts

apps/web/lib/mock-network-state.ts



Initial capability:



show map of stores, warehouse, and suppliers

filter by entity type

select date, initially mock date

click entity marker

open detail panel

show static metadata

show placeholder inventory summary

show placeholder daily action summary

10\. Network visualizer product design



The user lands on a map of Ontario/GTA operations.



They can:



Select a date.

See 15 stores, central warehouse, and supplier warehouses.

Click a store.

View inventory by category and product.

View stockout/spoilage risk summary.

View scheduled warehouse deliveries.

View agent-recommended daily actions.

Click warehouse.

View available-to-allocate inventory and inbound supplier deliveries.

Click supplier.

View products supplied, next delivery schedule, contract constraints, and reliability score.



Phase 1 version:



static/mock data only



Phase 2 version:



connect date selector to generated daily inventory snapshots



Phase 3 version:



overlay forecast and risk signals



Phase 4 version:



overlay warehouse allocation, transfer, and procurement decisions



Phase 5 version:



show agent decision traces and RAG evidence

11\. Data contracts required for the visualizer



The backend should eventually expose:



GET /api/network/nodes

GET /api/network/distance-matrix

GET /api/network/state?date=YYYY-MM-DD

GET /api/stores/{store\_id}/inventory?date=YYYY-MM-DD

GET /api/stores/{store\_id}/actions?date=YYYY-MM-DD

GET /api/warehouse/state?date=YYYY-MM-DD

GET /api/suppliers/{supplier\_id}/schedule?date=YYYY-MM-DD

GET /api/decisions?date=YYYY-MM-DD\&store\_id=...



Recommended TypeScript node shape:



export type NetworkNodeType = "store" | "warehouse" | "supplier";



export interface NetworkNode {

&#x20; id: string;

&#x20; type: NetworkNodeType;

&#x20; name: string;

&#x20; latitude: number;

&#x20; longitude: number;

&#x20; region?: string;

&#x20; categoryCoverage?: string\[];

&#x20; metadata: Record<string, string | number | boolean | string\[]>;

}



Recommended inventory summary shape:



export interface InventorySummary {

&#x20; date: string;

&#x20; nodeId: string;

&#x20; totalSkus: number;

&#x20; healthySkus: number;

&#x20; stockoutRiskSkus: number;

&#x20; spoilageRiskSkus: number;

&#x20; overstockRiskSkus: number;

&#x20; topItems: Array<{

&#x20;   skuId: string;

&#x20;   skuName: string;

&#x20;   category: string;

&#x20;   onHandUnits: number;

&#x20;   daysOfCover: number;

&#x20;   riskLevel: "low" | "medium" | "high";

&#x20; }>;

}



\## 12. Revised Phase 1 build order



\### Milestone 1A — Repo foundation



\- documentation foundation

\- Python package scaffold

\- `pyproject.toml`

\- GitHub Actions CI

\- basic tests



\### Milestone 1B — Domain model and schemas



\- Pydantic domain models

\- ERD in docs

\- schema validation tests

\- relationship validation tests



\### Milestone 1C — Network config and geospatial foundation



\- 15 stores

\- warehouse

\- suppliers with coordinates

\- generated network GeoJSON

\- generated distance matrix

\- tests for coordinate validity and nearest-store logic



\### Milestone 1D — SKU catalog and generation



\- category templates

\- 40 anchor SKUs

\- deterministic SKU generator

\- 500-SKU generated catalog

\- margin and shelf-life tests



\### Milestone 1E — Policy skeletons



\- parameter-aligned policy documents

\- document metadata front matter

\- policy loading tests



\### Milestone 1F — Network visualizer skeleton



\- Next.js app under `apps/web`

\- MapLibre map

\- entity markers

\- date selector placeholder

\- entity detail panel

\- mock network state

\- frontend lint/build command



\---



\## 13. Revised simulation plan



The simulator should be built in layers.



\### Simulation layer 1 — Static world state



Built in Phase 1:



\- stores

\- warehouse

\- suppliers

\- SKUs

\- policies

\- logistics constants

\- GeoJSON map nodes

\- distance matrix



\### Simulation layer 2 — Time and events



Built in Phase 2:



\- sales events

\- inventory events

\- warehouse receipt events

\- store delivery events

\- spoilage events

\- markdown events

\- stockout events

\- supplier delay events



\### Simulation layer 3 — Daily state snapshots



Also Phase 2:



\- store/SKU/day inventory

\- warehouse/SKU/day inventory

\- supplier inbound schedule

\- loss by store/SKU/day



\### Simulation layer 4 — Forecast and risk overlays



Built in Phase 3:



\- forecast demand

\- risk score

\- days of cover

\- stockout risk

\- spoilage risk

\- overstock risk



\### Simulation layer 5 — Decision overlays



Built in Phase 4 and Phase 5:



\- warehouse allocation

\- transfers

\- markdowns

\- procurement reviews

\- agent traces

\- expected savings

\- actual simulated outcome



\---



\## 14. Final decision summary



The project should go big, but not recklessly.



The map-based simulation visualizer is a strong product-level idea and should be introduced early as a skeleton.



The correct architecture is to separate:



\- static world definition

\- generated simulation state

\- forecast/risk overlays

\- operational decisions

\- agent decision traces

\- financial impact



The frontend should start with mock data shaped like the future API, while the backend builds the real operational engine underneath.



Major planning change:



> Add `Phase 1.6 — Interactive Network Visualizer Skeleton` to Phase 1.

