AGENTS.md - Codex Operating Guide for Itara Fresh Intelligence



This file keeps Codex aligned with the project. Read it before making changes. Follow it unless the user explicitly overrides it.



\---



\## Project identity



Project name: \*\*Itara Fresh Intelligence\*\*



Author: \*\*Kparobor Akpomiemie\*\*



Repository: https://github.com/Kparos000/Itara-Fresh-Intelligence



Formal description:



> An agentic replenishment intelligence system that forecasts demand, coordinates warehouse-to-store allocation, handles rare store-to-store transfer exceptions, triggers supplier procurement only at the network level, and verifies high-impact decisions against operational policy to reduce spoilage, stockouts, and inference cost across a grocery network.



Simple description:



> Itara Fresh Intelligence helps a grocery company decide what fresh inventory should move where, when, and why — using forecasts, policies, warehouse data, logistics constraints, and learned decision patterns to reduce waste and stockouts.



\---



\## Non-negotiable operating assumptions



1\. Itara Fresh orders from suppliers in bulk.

2\. Suppliers normally deliver to the main warehouse / distribution centre, not directly to stores.

3\. Store-level replenishment must check warehouse inventory before supplier procurement.

4\. Supplier purchase orders are network-level procurement decisions.

5\. A high-demand store does not automatically trigger supplier ordering.

6\. Store-to-store transfers are rare exception actions and should remain below 2% of replenishment actions.

7\. Forecasting predicts demand, but the agentic decision system decides what to do.

8\. The agent does not make decisions from memory. It must use tools, policy retrieval, forecasts, inventory, logistics constraints, financial simulation, and learned advisor output.

9\. Every savings claim must be generated from the simulation and financial loss engine, not hard-coded.

10\. The system must be token-cost aware. Do not use LLM calls for routine no-risk cases.



\---



\## Phase 1 map-visualizer decision



Phase 1 includes a lightweight \*\*Interactive Network Visualizer Skeleton\*\*.



This is not only a Phase 8 demo artifact. The visualizer must influence the data model from the beginning.



Phase 1 visualizer scope:



\- show 15 Ontario stores, one central warehouse, and supplier warehouse locations

\- use static/mock data at first

\- include a date selector placeholder

\- allow clicking stores, warehouse, and suppliers

\- open an entity detail panel

\- show placeholder inventory summary and daily action summary

\- use mock data shaped like future API responses



The full simulator will later attach daily inventory snapshots, forecasts, risk overlays, warehouse allocations, transfer routes, supplier schedules, agent actions, and financial impact to the same visual contract.



\---



\## Build philosophy



This is an operations-first AI/ML engineering project.



Correct mental model:



```text

Data tells us what happened.

Forecasting tells us what is likely to happen.

Risk detection tells us where action may be needed.

Warehouse allocation decides how existing stock should move.

Transfer logic handles rare exceptions.

Supplier procurement triggers only when the network is short.

RAG tells the agent what policies and contracts allow.

The learned advisor recommends what has worked in similar cases.

The agent coordinates tools, verifies constraints, and writes a trace.

Evals prove every layer works.

The demo tells the business story.

````



\---



\## Target architecture



Core modules should eventually look like this:



```text

src/itara/              # shared package root

src/itara/domain/       # domain entities and schema contracts

src/itara/config/       # config loading and validation

src/itara/geo/          # geospatial utilities, GeoJSON, distance matrix

src/itara/sim/          # event generation, simulation, financial loss engine

src/itara/ops/          # warehouse allocation, transfers, procurement, logistics

src/itara/ml/           # forecasting, features, risk detection

src/itara/rag/          # Qdrant indexing and retrieval

src/itara/agent/        # LangGraph flow, tools, decision traces

src/itara/learning/     # contextual bandit, rewards, learned advisor

src/itara/inference/    # model routing, token/cost logging

src/itara/api/          # FastAPI endpoints

apps/web/               # Next.js demo and map visualizer

reports/                # generated evaluation and business reports

data/config/            # static simulation configuration

data/policies/          # RAG policy documents

data/generated/         # generated datasets and simulation outputs

models/                 # trained model artifacts

```



\---



\## The 8 implementation phases



1\. \*\*Operational design, schema, simulation blueprint, and network visualizer skeleton\*\*

2\. \*\*Four-year event-stream simulator and financial loss engine\*\*

3\. \*\*Demand forecasting and risk detection\*\*

4\. \*\*Warehouse allocation, transfer exception, and procurement decision engine\*\*

5\. \*\*Agentic operations layer with MCP-style tools and RAG\*\*

6\. \*\*Learned decision advisor, contextual bandit, and token-aware routing\*\*

7\. \*\*Evals, observability, MLOps, and deployment\*\*

8\. \*\*Interactive demo, launch narrative, and portfolio packaging\*\*



\---



\## Agent behavior rules



The agent should only activate for action-required cases.



Action-required cases include:



\* high stockout risk

\* high spoilage risk

\* overstock risk

\* warehouse shortage risk

\* supplier timing risk

\* policy-sensitive decisions

\* high financial exposure

\* uncertainty requiring human review



The agent can output:



\* warehouse allocation request

\* warehouse-to-store delivery schedule

\* store-to-store transfer request

\* markdown instruction

\* supplier procurement review trigger

\* supplier purchase order recommendation

\* human escalation ticket

\* no action



The agent must always save a decision trace.



\---



\## Supplier procurement rule



Supplier procurement is not a store-level action.



Correct trigger:



```text

network forecast demand

> warehouse available inventory + inbound supplier orders - network safety stock

```



Then check:



\* supplier MOQ

\* delivery day

\* lead time

\* supplier availability

\* emergency order terms

\* warehouse capacity

\* shelf-life risk

\* category policy



\---



\## Store-to-store transfer rule



Transfer only if all conditions pass:



1\. Target store has high stockout risk before warehouse delivery can solve it.

2\. Source store has low forecast demand over the next 7 days.

3\. Source store remains above safety stock after transfer.

4\. Product has sufficient remaining shelf life.

5\. Distance is within allowed radius.

6\. Transfer can happen overnight or in approved delivery window.

7\. Transfer cost is lower than expected avoided loss.

8\. Warehouse allocation cannot solve the issue in time.



\---



\## RAG rule



Qdrant is the default vector database for the main demo because it gives a production-style self-hosted retrieval layer with metadata filtering.



FAISS may be implemented as an optional local fallback. Do not replace Qdrant as the default without explicit user approval.



RAG should be used for:



\* company policy

\* supplier contract terms

\* freshness standards

\* transfer rules

\* markdown rules

\* cold-chain requirements

\* escalation requirements



RAG should not be used for structured values that belong in tables, such as current stock, MOQ, lead time, delivery day, or store inventory. Those should come from tools/database queries.



\---



\## Learned advisor rule



The first implementation should use a contextual bandit as the learned decision advisor.



Do not make PPO or CQL required for the first launch. They can be research extensions after the contextual bandit and core agent flow work.



The learned advisor does not replace the agent. It returns structured recommendation data. The agent must verify that recommendation against policy, logistics, freshness, and financial constraints before execution.



Example learned advisor output:



```json

{

&#x20; "recommended\_action": "warehouse\_allocation\_plus\_transfer",

&#x20; "confidence": 0.74,

&#x20; "expected\_savings": 2330.0,

&#x20; "reason\_codes": \[

&#x20;   "target\_stockout\_before\_warehouse\_delivery",

&#x20;   "source\_store\_low\_forecast\_demand",

&#x20;   "transfer\_cost\_below\_lost\_margin"

&#x20; ]

}

```



\---



\## Evals required



Every major layer needs evals.



Required evaluation categories:



\* data realism checks

\* forecasting metrics: MAE, RMSE, WAPE, MAPE, bias, directional accuracy

\* risk detection precision/recall

\* decision quality and savings versus baseline

\* transfer rate guardrail

\* policy compliance rate

\* RAG retrieval and faithfulness

\* agent structured-output validity

\* decision trace completeness

\* inference cost and latency

\* business impact and ROI



\---



\## Coding standards



\* Prefer clear, typed Python.

\* Use Pydantic models for domain entities and contracts.

\* Keep simulation logic deterministic when a seed is provided.

\* Do not hard-code final savings numbers.

\* Separate generated data from source code.

\* Keep functions small and testable.

\* Add tests with each meaningful change.

\* Avoid hidden external API dependencies in core tests.

\* No secrets in code.

\* Prefer small, bounded pull-style changes over huge edits.

\* Keep public claims clearly labeled as modeled unless validated in real deployment.



\---



\## Codex repo scanning rule



Do not scan the entire repository on every prompt.



Preferred workflow:



1\. Read this file first.

2\. Read the user prompt carefully.

3\. Identify the smallest relevant area of the repo.

4\. Use targeted commands such as:



```bash

rg "keyword" path/to/relevant/area

ls path/to/relevant/area

sed -n '1,220p' path/to/file.py

```



5\. Avoid broad repo scans unless necessary.

6\. If broader context is needed, explain why.

7\. Summarize what files were inspected before making changes.



Avoid unless explicitly needed:



```bash

find . -type f

rg "" .

cat large\_file

```



\---



\## Git workflow



Before changing files:



```bash

git status --short

```



After code changes:



```bash

ruff format src tests

ruff check src tests

mypy src

pytest -q

```



For frontend changes under `apps/web`, run the relevant frontend checks once the app exists:



```bash

npm run lint

npm run build

```



When asked to commit and push, only do so after checks pass or after clearly reporting why a check could not be run.



Commit messages should be clear and specific, for example:



```text

Add project planning and operating guide

Add Phase 1 schema foundation

Add network geospatial config

Add network visualizer skeleton

```



\---



\## Documentation update rule



If a major project decision changes, ask whether `AGENTS.md` and/or `docs/project\_plan.md` should be updated so future Codex sessions do not lose the decision.



Major changes include:



\* data model changes

\* operating flow changes

\* new agent roles

\* new policy logic

\* new evaluation metrics

\* new phase boundaries

\* new directory structure

\* changes to warehouse, supplier, or store assumptions

\* changes to how RL/bandit is used

\* changes to model routing or inference-cost logic

\* changes to demo narrative or public claims



\---



\## Demo rules



The demo should start with business outcome, not architecture.



Demo story:



1\. Press-release style result

2\. Before vs after losses

3\. Map-based network simulator

4\. Agent decision replay

5\. Future planning console

6\. Engineering observability



Historical 2024-2025 agent decisions should be precomputed and saved. The live demo should activate the agent only for selected cases or small batches.



The map-based simulator should eventually allow the user to:



\* select a date

\* see all stores, warehouse, and suppliers

\* click a store to view inventory and daily action summary

\* click the warehouse to view available-to-allocate inventory and inbound deliveries

\* click a supplier to view products supplied and next delivery schedule

\* view warehouse allocation flows

\* view store-to-store transfer exceptions

\* view policy-grounded agent decisions

\* view expected and actual financial impact



\---



\## Network visualizer data contract



The frontend should initially use mock data shaped like future API responses.



Planned endpoints:



```text

GET /api/network/nodes

GET /api/network/distance-matrix

GET /api/network/state?date=YYYY-MM-DD

GET /api/stores/{store\_id}/inventory?date=YYYY-MM-DD

GET /api/stores/{store\_id}/actions?date=YYYY-MM-DD

GET /api/warehouse/state?date=YYYY-MM-DD

GET /api/suppliers/{supplier\_id}/schedule?date=YYYY-MM-DD

GET /api/decisions?date=YYYY-MM-DD\&store\_id=...

```



Recommended TypeScript node shape:



```ts

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

```



Recommended inventory summary shape:



```ts

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

```



\---



\## Communication style for Codex responses



When reporting back to the user:



\* be direct

\* explain what changed

\* list files changed

\* list tests run

\* include exact PowerShell commands when the user needs to run something

\* if something fails, report the error and likely fix

\* if context should be saved to `AGENTS.md`, ask the user first



\---



\## Current Phase 1 milestone order



1\. \*\*Milestone 1A — Repo foundation\*\*



&#x20;  \* documentation foundation

&#x20;  \* Python package scaffold

&#x20;  \* `pyproject.toml`

&#x20;  \* GitHub Actions CI

&#x20;  \* basic tests



2\. \*\*Milestone 1B — Domain model and schemas\*\*



&#x20;  \* Pydantic domain models

&#x20;  \* ERD

&#x20;  \* schema validation tests

&#x20;  \* relationship validation tests



3\. \*\*Milestone 1C — Network config and geospatial foundation\*\*



&#x20;  \* 15 stores

&#x20;  \* warehouse

&#x20;  \* suppliers with coordinates

&#x20;  \* network GeoJSON

&#x20;  \* distance matrix

&#x20;  \* geospatial tests



4\. \*\*Milestone 1D — SKU catalog and generation\*\*



&#x20;  \* category templates

&#x20;  \* 40 anchor SKUs

&#x20;  \* deterministic SKU generator

&#x20;  \* 500-SKU generated catalog

&#x20;  \* margin and shelf-life tests



5\. \*\*Milestone 1E — Policy skeletons\*\*



&#x20;  \* parameter-aligned policy documents

&#x20;  \* metadata front matter

&#x20;  \* policy loading tests



6\. \*\*Milestone 1F — Network visualizer skeleton\*\*



&#x20;  \* Next.js app under `apps/web`

&#x20;  \* MapLibre map

&#x20;  \* entity markers

&#x20;  \* date selector placeholder

&#x20;  \* entity detail panel

&#x20;  \* mock network state

&#x20;  \* frontend lint/build checks



7\. \*\*Milestone 1G — Phase 1 validation\*\*



&#x20;  \* final docs check

&#x20;  \* CI check

&#x20;  \* repo hygiene check

&#x20;  \* confirm Phase 1 exit criteria



````

