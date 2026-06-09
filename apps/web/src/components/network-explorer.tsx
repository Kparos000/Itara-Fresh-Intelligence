"use client";

import { createRef, useCallback, useMemo, useRef, useState } from "react";

import { NetworkMap } from "@/components/network-map";
import { NetworkNodeCard } from "@/components/network-node-card";
import type { NetworkNode } from "@/data/network";

export function NetworkExplorer({ nodes }: { nodes: NetworkNode[] }) {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const nodeRefs = useMemo(() => {
    return new Map(nodes.map((node) => [node.node_id, createRef<HTMLDivElement>()]));
  }, [nodes]);

  const inventoryPanelRef = useRef<HTMLDivElement | null>(null);

  const stores = nodes.filter((node) => node.node_type === "store");
  const suppliers = nodes.filter((node) => node.node_type === "supplier");
  const warehouses = nodes.filter((node) => node.node_type === "warehouse");

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
          </div>
        </div>

        <div className="mt-8">
          <NetworkMap
            nodes={nodes}
            selectedNodeId={selectedNodeId}
            onNodeSelect={handleNodeSelect}
          />
        </div>
      </div>

      <aside className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <h2 className="text-2xl font-bold text-white">Network inventory</h2>
        <p className="mt-2 text-sm text-slate-400">
          Selecting a map marker scrolls this panel to the matching node.
        </p>

        <div
          ref={inventoryPanelRef}
          className="mt-6 flex max-h-[720px] flex-col gap-3 overflow-y-auto pr-2"
        >
          <SectionTitle label="Warehouse" count={warehouses.length} />
          {warehouses.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <NetworkNodeCard
                node={node}
                isSelected={selectedNodeId === node.node_id}
              />
            </div>
          ))}

          <SectionTitle label="Stores" count={stores.length} />
          {stores.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <NetworkNodeCard
                node={node}
                isSelected={selectedNodeId === node.node_id}
              />
            </div>
          ))}

          <SectionTitle label="Suppliers" count={suppliers.length} />
          {suppliers.map((node) => (
            <div key={node.node_id} ref={nodeRefs.get(node.node_id)}>
              <NetworkNodeCard
                node={node}
                isSelected={selectedNodeId === node.node_id}
              />
            </div>
          ))}
        </div>
      </aside>
    </section>
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