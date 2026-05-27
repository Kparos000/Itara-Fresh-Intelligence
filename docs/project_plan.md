\# Itara Fresh Intelligence — Project Plan



Author: Kparobor Akpomiemie  

Repository: https://github.com/Kparos000/Itara-Fresh-Intelligence



\---



\## Formal description



Itara Fresh Intelligence is an agentic replenishment intelligence system that forecasts demand, coordinates warehouse-to-store allocation, handles rare store-to-store transfer exceptions, triggers supplier procurement only at the network level, and verifies high-impact decisions against operational policy to reduce spoilage, stockouts, and inference cost across a grocery network.



\## Simple description



Itara Fresh Intelligence helps a grocery company decide what fresh inventory should move where, when, and why — using forecasts, policies, warehouse data, logistics constraints, learned decision patterns, and policy-grounded agentic workflows.



\---



\## Planning principles



This project must be built as a business-loss reduction system, not as a generic AI-agent demo.



Core principles:



1\. Operations first, AI second.

2\. Warehouse-first replenishment.

3\. Supplier procurement is network-level.

4\. Store-to-store transfers are rare exceptions.

5\. Forecasting is necessary but not sufficient.

6\. The agent does not guess.

7\. Every claim must be measurable.

8\. The system must be token-cost aware.

9\. The map-based simulator should become a core product interface, not just a final presentation layer.



\---



\## Network simulation scope



The simulated operating network includes:



\- 15 stores in Ontario

\- 1 central warehouse / distribution centre

\- multiple suppliers by category

\- 500 perishable SKUs

\- four-year simulation timeline

\- future planning window up to 6 months



Store districts:



\- Old Toronto

\- North York

\- Scarborough

\- Etobicoke

\- York

\- East York

\- Mississauga



Product categories:



\- produce

\- dairy

\- meat

\- bakery

\- deli

\- seafood

\- prepared foods

\- floral



\---



\## Four-year timeline



| Year | Mode | Purpose |

|---|---|---|

| 2022 | Baseline operations | Establish first-year loss benchmark |

| 2023 | Baseline operations | Show problem growth and strengthen business case |

| 2024 | AI intervention starts | Deploy forecasts, risk detection, agent decisions, and policy checks |

| 2025 | AI intervention matures | Add learned advisor, token-aware routing, and improved allocation |



2024 should include a realistic soft launch:



\- January to March: observe, recommend, and escalate only

\- April to December: controlled execution with policy verification

\- 2025: mature execution with learned advisor and token-aware routing



\---



\## Primary business metrics



\- spoilage loss

\- stockout lost margin

\- markdown margin loss

\- transfer cost

\- holding cost

\- AI inference cost

\- net expected savings

\- policy compliance rate

\- escalation rate

\- store-to-store transfer rate



Every savings claim must be generated from the simulation and financial loss engine. Final public claims must not be hard-coded.



\---



\## Phase 1 — Operational design, schema, simulation blueprint, and network visualizer skeleton



Goal: define the full operating world before writing the agent.



Phase 1 now includes the map-based network visualizer skeleton because the map is core to the product experience and should influence backend data contracts from the beginning.



Subphases:



1\. Domain model and ERD

2\. Location and logistics model

3\. Supplier model

4\. Product and price model

5\. Policy document blueprint

6\. Interactive network visualizer skeleton



Phase 1 deliverables:



\- `AGENTS.md`

\- `docs/project\_plan.md`

\- `docs/phase1\_planning.md`

\- `docs/domain\_model.md`

\- `docs/architecture.md`

\- `data/config/stores.yaml`

\- `data/config/warehouse.yaml`

\- `data/config/suppliers.yaml`

\- `data/config/sku\_catalog.yaml`

\- `data/generated/network\_nodes.geojson`

\- `data/generated/distance\_matrix.csv` or `.parquet`

\- `data/policies/\*.md`

\- Python package scaffold

\- schema validation tests

\- GitHub Actions CI

\- initial `apps/web` visualizer skeleton



Exit criteria:



\- store, warehouse, supplier, SKU, logistics, and policy assumptions exist

\- schema validation passes

\- relationship checks pass

\- network map data can be generated

\- frontend visualizer can render static/mock network state

\- no agent implementation begins before operating assumptions are represented in schemas



\---



\## Phase 2 — Four-year event-stream simulator and financial loss engine



Goal: generate realistic replayable operations from 2022 to 2025 and calculate modeled financial loss.



Core outputs:



\- event stream

\- daily inventory state

\- spoilage events

\- stockout events

\- markdown events

\- transfer events

\- supplier delay events

\- supplier short-shipment events

\- agent decision events

\- annual loss reports

\- counterfactual replay



The simulator should use replayable event logs first, not Kafka. Live streaming can be simulated later with replay mode.



\---



\## Phase 3 — Demand forecasting and risk detection



Goal: forecast demand and convert forecasts into action-required cases.



Models:



\- naive moving average baseline

\- seasonal baseline

\- LightGBM production-style tabular model



Forecast horizons:



\- 1 day

\- 7 days

\- 14 days

\- 30 days

\- up to 6 months for planning



Forecasting predicts risk. It does not decide the action by itself.



\---



\## Phase 4 — Warehouse allocation, transfer exception, and procurement decision engine



Goal: build deterministic operating decision logic before adding heavy agentic reasoning.



Decision order:



1\. check store inventory

2\. check scheduled warehouse delivery

3\. check warehouse available-to-allocate inventory

4\. evaluate rare store-to-store transfer

5\. trigger supplier procurement only for network-level shortage

6\. simulate candidate action financial impact



Store-level demand spikes must not automatically create supplier orders.



\---



\## Phase 5 — Agentic operations layer with MCP-style tools and RAG



Goal: build the policy-grounded agentic workflow.



The agent coordinates tools, retrieves policies, checks supplier terms, reviews learned advisor output, runs financial simulation, verifies constraints, and writes decision traces.



The agent activates only for action-required, policy-sensitive, high-value, or uncertain cases.



\---



\## Phase 6 — Learned decision advisor, contextual bandit, and token-aware routing



Goal: add learning and inference-cost control.



First implementation should use contextual bandits. PPO and CQL are research extensions, not launch blockers.



The learned advisor recommends actions. It does not replace policy verification, logistics checks, or financial simulation.



\---



\## Phase 7 — Evals, observability, MLOps, and deployment



Goal: prove the system is credible, reproducible, and inspectable.



Includes:



\- evaluation suite

\- MLflow

\- CI/CD

\- Docker Compose

\- FastAPI

\- Qdrant

\- PostgreSQL

\- frontend build checks

\- observability dashboard



\---



\## Phase 8 — Interactive demo, launch narrative, and portfolio packaging



Goal: create a public-facing demo and portfolio story.



Demo sections:



1\. press-release landing page

2\. before vs after dashboard

3\. map-based network simulator

4\. agent decision replay

5\. future planning console

6\. engineering observability



\---



\## Recommended build order



1\. Project documentation and repo scaffold

2\. Python package scaffold and CI

3\. Domain models and schemas

4\. 15-store network, warehouse, suppliers, GeoJSON, distance matrix

5\. SKU catalog and generator

6\. Policy skeletons

7\. Network visualizer skeleton

8\. Event stream simulator

9\. Financial loss engine

10\. Forecasting

11\. Risk detector

12\. Warehouse allocation engine

13\. Transfer exception engine

14\. Procurement trigger logic

15\. Qdrant RAG

16\. Agent decision graph

17\. Decision trace ledger

18\. Contextual bandit advisor

19\. Token-aware routing

20\. Evals and launch demo

