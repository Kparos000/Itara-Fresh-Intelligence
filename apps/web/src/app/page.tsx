import { MetricCard } from "@/components/metric-card";
import { NetworkExplorer } from "@/components/network-explorer";
import { networkNodes, networkSummary } from "@/data/network";

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

        <NetworkExplorer nodes={networkNodes} />
      </section>
    </main>
  );
}