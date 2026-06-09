import type { NetworkNode, NetworkNodeType } from "@/data/network";

const nodeStyles: Record<NetworkNodeType, string> = {
  warehouse: "border-blue-300 bg-blue-50 text-blue-950",
  store: "border-emerald-300 bg-emerald-50 text-emerald-950",
  supplier: "border-amber-300 bg-amber-50 text-amber-950",
};

const selectedNodeStyles: Record<NetworkNodeType, string> = {
  warehouse: "ring-4 ring-blue-400",
  store: "ring-4 ring-emerald-400",
  supplier: "ring-4 ring-amber-400",
};

const nodeLabels: Record<NetworkNodeType, string> = {
  warehouse: "Warehouse",
  store: "Store",
  supplier: "Supplier",
};

export function NetworkNodeCard({
  node,
  isSelected = false,
}: {
  node: NetworkNode;
  isSelected?: boolean;
}) {
  return (
    <article
      className={`rounded-2xl border p-4 transition ${nodeStyles[node.node_type]} ${
        isSelected ? selectedNodeStyles[node.node_type] : ""
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide opacity-70">
            {nodeLabels[node.node_type]} · {node.region ?? "Unknown region"}
          </p>
          <h3 className="mt-1 text-lg font-bold">{node.node_name}</h3>
        </div>
        <span className="rounded-full bg-white/70 px-3 py-1 text-xs font-semibold">
          {node.node_id}
        </span>
      </div>

      <div className="mt-3 text-sm leading-6 opacity-80">
        <p>
          Latitude: {node.coordinates.latitude.toFixed(4)} · Longitude:{" "}
          {node.coordinates.longitude.toFixed(4)}
        </p>
        {node.category_coverage.length > 0 ? (
          <p className="mt-1">Categories: {node.category_coverage.join(", ")}</p>
        ) : null}
      </div>
    </article>
  );
}