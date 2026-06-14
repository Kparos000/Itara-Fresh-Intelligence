# AGENTS.md - Itara Fresh Intelligence Operating Guide

Read this file before making changes. It is the persistent operating guide for
Codex and other coding agents working in this repository. Follow it unless the
user explicitly overrides a rule for the current task.

## Project identity

- Project: **Itara Fresh Intelligence**
- Author: **Kparobor Akpomiemie**
- Repository: <https://github.com/Kparos000/Itara-Fresh-Intelligence>

## Project mission

Itara Fresh Intelligence is an operations-first replenishment intelligence
system for a fresh grocery network.

The system is intended to determine:

> What fresh inventory should move where, when, why, and with what modeled
> financial impact?

It models suppliers, a central warehouse, stores, perishable SKUs, inventory
events, demand, spoilage, stockouts, markdowns, transfers, supplier
procurement, policies, financial impact, forecasts, and later agentic and
learned decision support.

This is not a generic AI-agent demo. It is a business-loss reduction system
whose recommendations must be grounded in operational data, deterministic
logic, policy, logistics, and modeled financial outcomes.

## End-to-end system story

The intended system flow is:

1. Define the operating world: stores, warehouse, suppliers, SKUs, policies,
   logistics constraints, and distances.
2. Simulate replayable operations from 2022 through 2025.
3. Calculate spoilage loss, stockout lost margin, markdown margin loss,
   transfer cost, holding cost, inference cost, and net loss.
4. Forecast demand and detect operational risk.
5. Allocate available warehouse inventory to stores.
6. Use store-to-store transfers only as rare, policy-constrained exceptions.
7. Trigger supplier procurement only when the network is short.
8. Use RAG for unstructured policies and contracts, not for structured
   inventory or supplier values.
9. Activate agentic reasoning only for action-required, policy-sensitive, or
   high-exposure cases.
10. Verify recommendations against inventory, freshness, logistics, policy,
    and financial constraints.
11. Save an explainable decision trace.
12. Add a contextual-bandit advisor and token-aware model routing only after
    the simulator and deterministic decision baseline are reliable.
13. Present the result through a map-based operating console and business
    impact narrative.

The correct mental model is:

```text
Data tells us what happened.
Simulation creates replayable operating history.
Forecasting tells us what is likely to happen.
Risk detection identifies where action may be needed.
Warehouse allocation decides how existing stock should move.
Transfer logic handles rare exceptions.
Supplier procurement triggers only when the network is short.
RAG provides policy and contract evidence.
The agent coordinates tools, verifies constraints, and writes a trace.
The learned advisor recommends patterns; it does not bypass verification.
Evals prove each layer works.
The demo explains the business outcome.
```

## Current phase status

### Phase 1: Static operating world and visual shell

Status: **substantially implemented**.

Implemented backend foundation:

- Python package and CI foundation
- typed Pydantic domain models
- configuration loading and validation
- 15 Ontario stores
- 1 central warehouse
- 10 suppliers
- deterministic 500-SKU catalog with 40 anchor SKUs
- policy documents and policy loading
- geospatial utilities
- generated network nodes and directed distance matrix
- Phase 1 validation command and tests

Implemented frontend foundation:

- Next.js application under `apps/web`
- TypeScript, Tailwind, and MapLibre
- backend-generated network JSON
- 15 stores, 10 suppliers, and 1 warehouse on the map
- search and node-type filters
- clickable markers and popups
- side-panel selection and scrolling
- Supplier -> Warehouse relationship overlay
- Warehouse -> Store relationship overlay
- two static Store -> Store transfer exception examples
- independent route toggles
- operational flow summary

The current map routes are relationship and operating-flow overlays. They are
not optimized roads, truck routes, dispatch schedules, or recommendations from
an allocation engine.

### Phase 2: Event-stream simulator and financial loss engine

Status: **started**.

Implemented:

- typed simulator event schemas
- stable event types
- validation for quantities, financial values, and key event relationships
- pure financial loss formulas
- immutable financial impact summary contract
- tests for event and financial contracts

Not yet implemented:

- event generator
- deterministic seeded simulation engine
- inventory state transitions
- daily event replay
- multi-day or four-year generated event streams
- daily financial impact aggregation
- baseline-versus-intervention reports
- generated simulation datasets

### Future phases

The following are planned but not yet implemented:

- Phase 3: demand forecasting and risk detection
- Phase 4: warehouse allocation, transfer eligibility, and procurement engine
- Phase 5: FastAPI tools, Qdrant RAG, and policy-grounded agent flow
- Phase 6: contextual-bandit advisor and token-aware inference routing
- Phase 7: evals, observability, MLOps, and deployment
- Phase 8: full interactive demo, launch narrative, and portfolio packaging

Do not describe future phases as implemented.

## Non-negotiable operating assumptions

These rules must not change without explicit user approval:

1. Itara Fresh orders from suppliers in bulk.
2. Suppliers normally deliver to the central warehouse, not directly to
   stores.
3. Store replenishment checks warehouse inventory before supplier
   procurement.
4. The warehouse is the normal source of store replenishment.
5. A store-level demand spike does not automatically trigger supplier
   procurement.
6. Supplier purchase orders are network-level decisions.
7. Store-to-store transfers are rare exceptions, not normal replenishment.
8. Transfer actions should remain below 2% of replenishment actions unless a
   documented stress test intentionally changes the guardrail.
9. Forecasting predicts demand and risk; it does not execute decisions.
10. The agent must not decide from memory alone. It must use tools, retrieved
    policy, forecasts, inventory, logistics constraints, financial
    simulation, and any learned-advisor output.
11. Routine no-risk cases should use deterministic logic, not LLM calls.
12. Every savings claim must come from simulation and financial calculations.
13. Do not hard-code final savings or ROI claims.
14. Inference cost is part of total business cost.
15. Public claims must be labeled as modeled unless validated in a real
    deployment.

## Procurement rule

Supplier procurement is not a store-level action. The intended trigger is:

```text
network forecast demand
> warehouse available inventory
  + inbound supplier orders
  - network safety stock
```

Then verify supplier MOQ, delivery day, lead time, supplier availability,
emergency terms, warehouse capacity, shelf-life risk, and category policy.

## Transfer exception rule

A store-to-store transfer may be recommended only when all relevant conditions
pass:

1. The target store has high stockout risk before warehouse delivery can solve
   it.
2. The source store has low forecast demand over the next seven days.
3. The source remains above safety stock after transfer.
4. The product has sufficient remaining shelf life.
5. Distance is within the allowed radius.
6. The transfer fits an approved delivery window.
7. Transfer cost is lower than expected avoided loss.
8. Warehouse allocation cannot solve the issue in time.

## RAG and learned-advisor rules

Qdrant is the planned default vector database for the main demo. FAISS may be
an optional local fallback, but must not replace Qdrant as the default without
user approval.

Use RAG for unstructured evidence such as:

- company policy
- supplier contract terms
- freshness standards
- transfer rules
- markdown rules
- cold-chain requirements
- escalation requirements

Do not use RAG for structured current values such as stock, MOQ, lead time,
delivery day, or store inventory. Those values must come from validated
configuration, simulation state, database queries, or tools.

The first learned advisor should be a contextual bandit. PPO and CQL are
optional research extensions, not launch requirements. The advisor returns a
structured recommendation; the decision layer must still verify policy,
logistics, freshness, and financial constraints.

## Architecture and folder map

```text
src/itara/
  domain/       # Pydantic domain entities and shared contracts
  config/       # configuration loading and validation
  geo/          # distances, network nodes, and generated map artifacts
  sim/          # event contracts, future simulator, and financial formulas
  ops/          # future allocation, transfer, procurement, and logistics logic
  ml/           # future features, forecasting, and risk detection
  rag/          # policy loading and future Qdrant retrieval
  agent/        # future tools, orchestration, and decision traces
  learning/     # future contextual bandit, rewards, and learned advisor
  inference/    # future model routing and token/cost logging
  api/          # future FastAPI endpoints
  utils/        # shared utilities

apps/web/
  src/app/        # Next.js routes and page shell
  src/components/ # map and visualizer components
  src/data/       # generated network JSON and TypeScript contracts

data/
  config/       # static network and SKU configuration
  policies/     # retrieval-ready policy documents
  generated/    # reproducible generated artifacts and future simulation output

docs/           # project plan, checkpoints, and design documentation
reports/        # future generated evaluation and business reports
models/         # future trained model artifacts
tests/          # deterministic backend tests
```

Respect module boundaries:

- domain models must not depend on infrastructure or frontend code
- simulation logic must not depend on the frontend
- pure financial functions must not log or mutate state
- agent logic must use tools/contracts rather than reaching into unrelated
  modules
- API code should translate between external requests and internal services
- frontend code should consume stable contracts rather than duplicate business
  logic

When working under `apps/web`, also read and follow `apps/web/AGENTS.md`. A
deeper `AGENTS.md` overrides this file for its subtree when rules conflict.

## Coding standards

- Prefer clear, typed Python.
- Use Pydantic models for domain and boundary contracts.
- Use enums for stable event, action, risk, and status values.
- Keep modules focused and functions small.
- Use guard clauses instead of deep nesting.
- Validate inputs at system boundaries and fail fast.
- Use meaningful error messages that name the invalid field.
- Never swallow errors silently.
- Keep pure calculations free of logging, global mutation, and I/O.
- Keep simulation deterministic whenever a seed is provided.
- Avoid hidden randomness and live external services in core tests.
- Separate generated data from source code.
- Do not commit heavy generated artifacts unless explicitly requested.
- Do not add dependencies without a clear need.
- Never commit secrets, credentials, `.env`, or private tokens.
- Add tests with every meaningful behavioral change.
- Test edge cases and invalid inputs, not only happy paths.
- Comment the reason for non-obvious logic, not the obvious mechanics.
- Keep public functions and important contracts documented.
- Avoid unrelated refactors and formatting churn.
- Keep changes bounded to the requested ownership area.

## Required checks

Run from the repository root for backend or cross-cutting changes:

```powershell
ruff format src tests
ruff check src tests
mypy src
pytest -q
```

Phase 1 validation can also be run when network/configuration contracts change:

```powershell
python -c "from itara.validation import main; main()"
```

Run from `apps/web` for frontend changes:

```powershell
npm run lint
npm run build
```

For manual frontend verification:

```powershell
npm run dev
```

Then open:

```text
http://localhost:3000
```

Do not report a check as passing unless it was actually run. If a check cannot
run, report the exact failure and likely remediation.

## Git and push rules

1. Run `git status --short` before editing.
2. Preserve unrelated user changes in a dirty worktree.
3. Stage only files relevant to the requested change.
4. Keep commits atomic: one logical change per commit.
5. Use clear, specific commit messages.
6. Run the relevant required checks before committing.
7. Do not push broken code unless the user explicitly instructs it and the
   failure is documented.
8. Do not rewrite history, force-push, or use destructive reset commands unless
   explicitly requested.
9. When asked to commit and push, confirm the final branch and worktree state.

Example commit messages:

```text
Add simulator event schemas
Add financial loss calculation foundation
Add supplier inbound route overlay
Restore project operating guide
```

## Codex context-management rules

1. Read this file before making changes.
2. Read the user request carefully and classify it as backend, frontend,
   documentation, or cross-cutting.
3. Inspect the smallest relevant area first.
4. Use targeted commands such as:

   ```powershell
   rg "keyword" path\to\relevant\area
   Get-ChildItem path\to\relevant\area
   Get-Content path\to\file
   ```

5. Do not scan the entire repository on every prompt.
6. Avoid broad commands such as recursive dumps of every file unless the task
   genuinely requires repository-wide analysis.
7. If broader context is needed, explain why before expanding the scan.
8. Summarize the files inspected before making substantial edits.
9. Do not rewrite unrelated files.
10. Do not infer that an empty module directory means a feature is implemented.
11. Distinguish current implementation, scaffolding, and future plans in code,
    documentation, and user-facing reports.
12. Preserve the warehouse-first, network-procurement, rare-transfer, and
    modeled-savings rules.
13. Keep a task within the requested phase unless the user approves a phase or
    architecture change.
14. Do not jump to LangGraph, RAG infrastructure, or RL before the simulator,
    financial engine, forecasting, and deterministic decision baseline are
    ready.
15. Report changed files, checks run, failures, and final git status directly.

## Documentation and decision updates

Major user-approved decisions must not be left only in chat history.

Ask whether to update `AGENTS.md`, `docs/project_plan.md`, and/or an ADR under
`docs/decisions/` when a decision changes:

- operating flow
- domain or API contracts
- warehouse, supplier, store, or SKU assumptions
- procurement or transfer policy
- evaluation metrics
- phase boundaries
- directory structure
- agent roles or tool boundaries
- RAG provider or retrieval rules
- contextual-bandit or RL placement
- inference routing or token-cost logic
- demo narrative or public claims

After the user approves the decision, update the relevant documentation in the
same focused change or the next explicitly requested documentation change.

## Current next work

The recommended sequence from the current repository state is:

1. Add a deterministic daily simulator state model.
2. Implement seeded generation for a small, bounded event window.
3. Apply events to inventory state transitions.
4. Aggregate daily financial impact from events.
5. Add realism and invariant checks for generated operations.
6. Expand carefully toward the four-year 2022-2025 replay.
7. Build forecasting training tables and baseline forecasts.
8. Add risk detection.
9. Build deterministic warehouse-first allocation logic.
10. Add transfer eligibility and network procurement logic.
11. Introduce API, RAG, and agent tooling only after those foundations are
    tested.

Do not create huge generated datasets during early simulator work. Start with
small deterministic samples and scale only after contracts and invariants are
stable.

## Evaluation expectations

Every major layer requires evidence:

- data realism and invariant checks
- forecasting MAE, RMSE, WAPE, MAPE, bias, and directional accuracy
- risk detection precision and recall
- decision quality and modeled savings versus baseline
- transfer-rate guardrail
- policy compliance
- RAG retrieval quality and faithfulness
- structured agent output validity
- decision-trace completeness
- inference cost and latency
- modeled business impact and ROI

## Honesty and communication rules

Use precise language about project maturity.

Accurate examples:

```text
Implemented simulator event schemas.
Implemented the financial formula foundation.
Added static operating-flow route overlays.
Started Phase 2 simulator work.
```

Do not claim:

```text
Built the full four-year simulator.
Optimized delivery routes.
Proved real-world savings.
Implemented the production agent.
Implemented reinforcement learning.
```

When reporting to the user:

- be direct
- explain what changed
- list modified files
- list checks run
- report failures and likely fixes
- provide exact PowerShell commands when the user must run something
- state whether changes were committed and pushed

The guiding rule is: write code and documentation for the project owner who
will return months later and need to understand the system quickly and safely.
