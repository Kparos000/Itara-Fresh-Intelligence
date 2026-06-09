import { MetricCard } from "@/components/metric-card";
import { NetworkMap } from "@/components/network-map";
import { NetworkNodeCard } from "@/components/network-node-card";
import { networkNodes, networkSummary } from "@/data/network";

const stores = networkNodes.filter((node) => node.node_type === "store");
const suppliers = networkNodes.filter((node) => node.node_type === "supplier");
const warehouses = networkNodes.filter((node) => node.node_type === "warehouse");

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 px-8 py-10 text-white">
      <section className="mx-auto max-w-7xl">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-emerald-400">
          Itara Fresh Intelligence
        </p>

        <h1 className="mt-6 text-5xl font-bold tracking-tight">
          Fresh Grocery Network Visualizer
        </h1>

        <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">
          A visual operating layer for stores, suppliers, warehouse inventory,
          policy-grounded replenishment, and future agentic decision traces.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-3 lg:grid-cols-6">
          <MetricCard label="Stores" value={networkSummary.node_type_counts.store} />
          <MetricCard label="Suppliers" value={networkSummary.node_type_counts.supplier} />
          <MetricCard label="Warehouse" value={networkSummary.node_type_counts.warehouse} />
          <MetricCard label="Total nodes" value={networkSummary.total_nodes} />
          <MetricCard
            label="Distance rows"
            value={networkSummary.distance_matrix_entries}
          />
          <MetricCard
            label="Max drive mins"
            value={networkSummary.max_estimated_drive_minutes.toFixed(0)}
          />
        </div>

        <section className="mt-10 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h2 className="text-2xl font-bold">Live network map</h2>
                <p className="mt-3 text-slate-400">
                  This map renders all backend-generated stores, suppliers, and the
                  central warehouse using their real latitude and longitude.
                </p>
              </div>

              <div className="flex flex-wrap gap-3 text-sm">
                <LegendDot label="Warehouse" className="bg-blue-400" />
                <LegendDot label="Store" className="bg-emerald-400" />
                <LegendDot label="Supplier" className="bg-amber-400" />
              </div>
            </div>

            <div className="mt-8">
              <NetworkMap nodes={networkNodes} />
            </div>
          </div>

          <aside className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-2xl font-bold text-white">Network inventory</h2>
            <p className="mt-2 text-sm text-slate-400">
              These cards are loaded from the generated backend network contract.
            </p>

            <div className="mt-6 flex max-h-[720px] flex-col gap-3 overflow-y-auto pr-2">
              <SectionTitle label="Warehouse" count={warehouses.length} />
              {warehouses.map((node) => (
                <NetworkNodeCard key={node.node_id} node={node} />
              ))}

              <SectionTitle label="Stores" count={stores.length} />
              {stores.map((node) => (
                <NetworkNodeCard key={node.node_id} node={node} />
              ))}

              <SectionTitle label="Suppliers" count={suppliers.length} />
              {suppliers.map((node) => (
                <NetworkNodeCard key={node.node_id} node={node} />
              ))}
            </div>
          </aside>
        </section>
      </section>
    </main>
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