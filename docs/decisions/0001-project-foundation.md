\# ADR 0001 — Project Foundation and Phase 1 Map Visualizer



Date: 2026-05-27



\## Status



Accepted



\---



\## Context



Itara Fresh Intelligence is being built as an operations-first AI/ML engineering project.



The project requires a credible grocery operating model before building forecasting, decision engines, RAG, or agentic workflows.



The original project plan placed the interactive demo mostly near the end of the roadmap. However, the map-based network simulator is not only a final presentation artifact. It is a core product interface.



Because the map visualizer will eventually show stores, warehouse inventory, suppliers, delivery schedules, risk signals, agent decisions, transfer routes, and financial impact, it should influence backend data contracts from the beginning.



\---



\## Decision



Phase 1 will include a lightweight \*\*Interactive Network Visualizer Skeleton\*\*.



The project will begin with:



\- public project plan

\- Codex operating guide

\- Phase 1 planning document

\- Python package scaffold

\- CI/CD

\- schema validation

\- geospatial network foundation

\- frontend visualizer skeleton



The map visualizer will start with static/mock data and later connect to generated simulation state.



Phase 1 visualizer scope:



\- show 15 Ontario stores, one central warehouse, and supplier warehouse locations

\- use static/mock data at first

\- include a date selector placeholder

\- allow clicking stores, warehouse, and suppliers

\- open an entity detail panel

\- show placeholder inventory summary and daily action summary

\- use mock data shaped like future API responses



\---



\## Consequences



Positive consequences:



\- frontend and backend contracts evolve together

\- the demo vision influences the domain model early

\- map data, GeoJSON, and distance matrix become first-class artifacts

\- future Codex prompts remain aligned with the product direction

\- the project becomes more product-like and less like a notebook-only ML demo



Tradeoffs:



\- Phase 1 becomes slightly larger

\- frontend setup begins earlier than originally planned

\- the team must avoid overbuilding the visualizer before the simulator exists



\---



\## Guardrails



The Phase 1 visualizer must remain a skeleton.



It should not block the backend operating model.



It should not require real simulation data in Phase 1.



It should use mock data shaped like the future API contract.



No final savings claims should be hard-coded into the visualizer.



\---



\## Alternatives considered



\### Wait until Phase 8 to build the visualizer



Rejected.



This would delay UX/data-contract discovery too long and may cause backend models to miss fields required by the product experience.



\### Build full frontend before simulator



Rejected.



This would over-prioritize UI before operational correctness.



\### Build lightweight visualizer skeleton in Phase 1



Accepted.



This creates the right balance between product vision and engineering discipline.

