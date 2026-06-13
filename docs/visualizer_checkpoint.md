# Phase 1 Visualizer Checkpoint

## Status

The Phase 1 network visualizer provides a working static view of the Itara Fresh operating network. It establishes the visual shell and data relationships that later simulation, forecasting, decision, and agent layers will extend.

## Current capabilities

The visualizer currently:

- runs as a Next.js application under `apps/web`
- renders a real MapLibre map
- loads backend-generated network JSON
- displays 15 stores, 10 suppliers, and 1 central warehouse
- supports node search and type filters
- provides clickable map markers and node popups
- scrolls the inventory side panel to the selected node
- shows supplier-to-warehouse inbound relationships
- shows warehouse-to-store replenishment relationships
- shows two static store-to-store transfer exception examples
- allows each route overlay to be toggled independently
- summarizes the intended operating flow: suppliers feed the warehouse, the warehouse replenishes stores, and store transfers remain rare exceptions

## Route overlay interpretation

The current route overlays are **relationship and operating-flow overlays, not optimized route plans**.

They communicate the direction and role of inventory movement in the Itara Fresh operating model:

- suppliers deliver bulk inventory to the central warehouse
- the warehouse is the normal source of store replenishment
- store-to-store transfers are limited exception actions

The lines do not yet represent optimized roads, vehicle routes, delivery sequences, dispatch schedules, capacity plans, travel-time decisions, or recommendations produced by an allocation engine.

## Not yet implemented

The visualizer does not yet provide:

- date-driven network state or historical replay
- SKU-level inventory snapshots
- simulated demand, sales, spoilage, stockouts, or financial losses
- forecasts, uncertainty, or operational risk overlays
- optimized warehouse allocations or delivery schedules
- policy-evaluated transfer recommendations
- network-level supplier procurement decisions
- live agent actions, tool calls, policy citations, or decision traces
- expected-versus-actual financial impact
- production API-backed state updates

The current transfer lines are static examples for communicating the exception concept. They are not evidence that a transfer is operationally justified.

## Support for later phases

### Phase 2: Simulation

The existing node and route structure provides the map contract for attaching daily inventory snapshots, inbound deliveries, demand events, spoilage, stockouts, and modeled financial loss. Date-based replay can replace the current static state without redesigning the core interface.

### Phase 3: Forecast and risk overlays

Forecast outputs can be attached to stores and SKUs, while map styling can show stockout, spoilage, overstock, warehouse shortage, and supplier timing risk. The current selection and detail-panel behavior provides a place to explain risk drivers and uncertainty.

### Phase 4: Decision overlays

Static relationship lines can evolve into dated warehouse allocations, delivery schedules, approved transfer exceptions, markdown actions, and network-level procurement recommendations. These overlays must come from deterministic operating logic and constraint checks rather than from the current examples.

### Phase 5: Agent traces

The visualizer can replay policy-grounded agent decisions by linking selected nodes and routes to tool inputs, retrieved policy evidence, financial simulation, approvals, escalations, and saved decision traces. Routine no-risk cases should remain outside expensive agent workflows.

## Checkpoint conclusion

The Phase 1 visualizer is a functional operating-world interface, not yet an optimization or decision system. Its purpose is to make the network structure and replenishment rules understandable now while preserving a stable visual contract for later operational intelligence.
