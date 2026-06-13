"use client";

import { createRef, useCallback, useMemo, useState } from "react";

import { NetworkMap } from "@/components/network-map";
import { NetworkNodeCard } from "@/components/network-node-card";
import type { NetworkNode, NetworkNodeType } from "@/data/network";

type NodeFilter = "all" | NetworkNodeType;

const filterLabels: Record<NodeFilter, string> = {
  all: "All",
  warehouse: "Warehouse",
  store: "Stores",
  supplier: "Suppliers",
};

export function NetworkExplorer({ nodes }: { nodes: NetworkNode[] }) {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState<NodeFilter>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [showSupplierRoutes, setShowSupplierRoutes] = useState(true);
  const [showWarehouseRoutes, setShowWarehouseRoutes] = useState(true);

  const nodeRefs = useMemo(() => {
    return new Map(nodes.map((node) => [node.node_id, createRef<HTMLDivElement>()]));
  }, [nodes]);

  const filteredNodes = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();

    return nodes.filter((node) => {
      const matchesFilter =
        activeFilter === "all" || node.node_type === activeFilter;

      const searchableText = [
        node.node_id,
        node.node_name,
        node.node_type,
        node.region ?? "",
        node.category_coverage.join(" "),
      ]
        .join(" ")
        .toLowerCase();

      const matchesSearch =
        normalizedQuery.length === 0 || searchableText.includes(normalizedQuery);

      return matchesFilter && matchesSearch;
    });
  }, [activeFilter, nodes, searchQuery]);

  const stores = filteredNodes.filter((node) => node.node_type === "store");
  const suppliers = filteredNodes.filter((node) => node.node_type === "supplier");
  const warehouses = filteredNodes.filter((node) => node.node_type === "warehouse");
  const supplierCount = nodes.filter(
    (node) => node.node_type === "supplier",
  ).length;
  const storeCount = nodes.filter((node) => node.node_type === "store").length;

  const handleNodeSelect = useCallback(
    (nodeId: string) => {
      setSelectedNodeId(nodeId);

      window.setTimeout(() => {
        const selectedRef = nodeRefs.get(nodeId);
        selectedRef?.current?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }, 80);
    },
    [nodeRefs],
  );

  return (
    <section className="mt-10 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-2xl font-bold">Live network map</h2>
            <p className="mt-3 text-slate-400">
              Click any marker to view its summary and jump to the matching
              inventory card.
            </p>
          </div>

          <div className="flex flex-wrap gap-3 text-sm">
            <LegendDot label="Warehouse" className="bg-blue-400" />
            <LegendDot label="Store" className="bg-emerald-400" />
            <LegendDot label="Supplier" className="bg-amber-400" />

            <button
              type="button"
              onClick={() => setShowSupplierRoutes((current) => !current)}
              className={`rounded-full px-4 py-2 font-semibold transition ${
                showSupplierRoutes
                  ? "bg-amber-400 text-slate-950"
                  : "bg-slate-950 text-slate-300 ring-1 ring-white/10 hover:bg-slate-800"
              }`}
            >
              Supplier → Warehouse routes{" "}
              {showSupplierRoutes ? "shown" : "hidden"}
            </button>

            <button
              type="button"
              onClick={() => setShowWarehouseRoutes((current) => !current)}
              className={`rounded-full px-4 py-2 font-semibold transition ${
                showWarehouseRoutes
                  ? "bg-blue-400 text-slate-950"
                  : "bg-slate-950 text-slate-300 ring-1 ring-white/10 hover:bg-slate-800"
              }`}
            >
              Warehouse → Store routes {showWarehouseRoutes ? "shown" : "hidden"}
            </button>
          </div>
        </div>

        <div className="mt-4 rounded-2xl border border-blue-400/30 bg-blue-400/10 p-4 text-sm leading-6 text-blue-100">
          <strong>Overlay meaning:</strong> amber dashed lines show supplier
          deliveries into the central warehouse. Blue dashed lines show normal
          outbound replenishment from the warehouse to stores.
        </div>

        <div className="mt-6 rounded-2xl border border-slate-700 bg-slate-950/70 p-4">
          <div>
            <h3 className="font-bold text-white">Operational flow summary</h3>
            <p className="mt-1 text-sm leading-6 text-slate-400">
              Suppliers feed the warehouse, the warehouse replenishes stores, and
              store-to-store transfers are reserved for rare exceptions.
            </p>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <FlowMetric
              label="Supplier inbound nodes"
              value={supplierCount.toString()}
            />
            <FlowMetric
              label="Warehouse outbound routes"
              value={storeCount.toString()}
            />
            <FlowMetric label="Transfer exceptions" value="0 planned" />
          </div>
        </div>

        <div className="mt-8">
          <NetworkMap
            nodes={filteredNodes}
            selectedNodeId={selectedNodeId}
            showSupplierRoutes={showSupplierRoutes}
            showWarehouseRoutes={showWarehouseRoutes}
            onNodeSelect={handleNodeSelect}
          />
        </div>
      </div>

      <aside className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <div className="flex flex-col gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white">Network inventory</h2>
            <p className="mt-2 text-sm text-slate-400">
              Search, filter, and select any generated network node.
            </p>
          </div>

          <input
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            placeholder="Search store, supplier, region, or category..."
            className="rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none ring-0 placeholder:text-slate-500 focus:border-emerald-400"
          />

          <div className="flex flex-wrap gap-2">
            {(Object.keys(filterLabels) as NodeFilter[]).map((filter) => (
              <button
                key={filter}
                type="button"
                onClick={() => setActiveFilter(filter)}
                className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                  activeFilter === filter
                    ? "bg-emerald-400 text-slate-950"
                    : "bg-slate-950 text-slate-300 ring-1 ring-white/10 hover:bg-slate-800"
                }`}
              >
                {filterLabels[filter]}
              </button>
            ))}
          </div>

          <p className="text-sm text-slate-400">
            Showing {filteredNodes.length} of {nodes.length} nodes
          </p>
        </div>

        <div className="mt-6 flex max-h-[720px] flex-col gap-3 overflow-y-auto pr-2">
          <SectionTitle label="Warehouse" count={warehouses.length} />
          {warehouses.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <button
                type="button"
                onClick={() => handleNodeSelect(node.node_id)}
                className="w-full text-left"
              >
                <NetworkNodeCard
                  node={node}
                  isSelected={selectedNodeId === node.node_id}
                />
              </button>
            </div>
          ))}

          <SectionTitle label="Stores" count={stores.length} />
          {stores.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <button
                type="button"
                onClick={() => handleNodeSelect(node.node_id)}
                className="w-full text-left"
              >
                <NetworkNodeCard
                  node={node}
                  isSelected={selectedNodeId === node.node_id}
                />
              </button>
            </div>
          ))}

          <SectionTitle label="Suppliers" count={suppliers.length} />
          {suppliers.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <button
                type="button"
                onClick={() => handleNodeSelect(node.node_id)}
                className="w-full text-left"
              >
                <NetworkNodeCard
                  node={node}
                  isSelected={selectedNodeId === node.node_id}
                />
              </button>
            </div>
          ))}
        </div>
      </aside>
    </section>
  );
}

function FlowMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-2 text-lg font-bold text-slate-100">{value}</p>
    </div>
  );
}

function LegendDot({
  label,
  className,
}: {
  label: string;
  className: string;
}) {
  return (
    <div className="flex items-center gap-2 rounded-full bg-slate-950 px-3 py-2 text-slate-300 ring-1 ring-white/10">
      <span className={`h-3 w-3 rounded-full ${className}`} />
      <span>{label}</span>
    </div>
  );
}

function SectionTitle({ label, count }: { label: string; count: number }) {
  return (
    <div className="sticky top-0 z-10 mt-2 rounded-xl bg-slate-900 py-2 text-sm font-bold uppercase tracking-[0.2em] text-slate-400">
      {label} · {count}
    </div>
  );
}
