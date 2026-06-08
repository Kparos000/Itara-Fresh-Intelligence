import { MapPin } from "@/components/map-pin";
import { MetricCard } from "@/components/metric-card";
import { NetworkNodeCard } from "@/components/network-node-card";
import { networkNodes, networkSummary } from "@/data/network";

const featuredNodeIds = [
  "warehouse_001",
  "store_001",
  "store_004",
  "store_006",
  "store_014",
  "supplier_001",
];

const mapPositions: Record<string, string> = {
  warehouse_001: "left-[45%] top-[42%]",
  store_001: "left-[52%] top-[58%]",
  store_004: "left-[56%] top-[30%]",
  store_006: "left-[73%] top-[35%]",
  store_014: "left-[28%] top-[70%]",
  supplier_001: "left-[8%] top-[82%]",
};

const featuredNodes = networkNodes.filter((node) =>
  featuredNodeIds.includes(node.node_id),
);

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
            <h2 className="text-2xl font-bold">Network map placeholder</h2>
            <p className="mt-3 text-slate-400">
              This visual shell is now driven by backend-generated network
              artifacts. Next, we will replace the placeholder with a real map.
            </p>

            <div className="mt-8 h-[520px] rounded-2xl border border-slate-800 bg-slate-950 p-6">
              <div className="relative h-full">
                {featuredNodes.map((node) => (
                  <MapPin
                    key={node.node_id}
                    node={node}
                    className={mapPositions[node.node_id] ?? "left-[50%] top-[50%]"}
                  />
                ))}
              </div>
            </div>
          </div>

          <aside className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-2xl font-bold text-white">Featured nodes</h2>
            <p className="mt-2 text-sm text-slate-400">
              These cards are loaded from the generated backend network contract.
            </p>

            <div className="mt-6 flex flex-col gap-3">
              {featuredNodes.map((node) => (
                <NetworkNodeCard key={node.node_id} node={node} />
              ))}
            </div>
          </aside>
        </section>
      </section>
    </main>
  );
}