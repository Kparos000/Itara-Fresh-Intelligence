import type { NetworkNode, NetworkNodeType } from "@/data/network";

const nodeColorClasses: Record<NetworkNodeType, string> = {
  warehouse: "bg-blue-400",
  store: "bg-emerald-400",
  supplier: "bg-amber-400",
};

const nodeLabelClasses: Record<NetworkNodeType, string> = {
  warehouse: "text-blue-100",
  store: "text-emerald-100",
  supplier: "text-amber-100",
};

export function MapPin({
  node,
  leftPercent,
  topPercent,
}: {
  node: NetworkNode;
  leftPercent: number;
  topPercent: number;
}) {
  return (
    <div
      className="absolute"
      style={{
        left: `${leftPercent}%`,
        top: `${topPercent}%`,
      }}
    >
      <div className="flex -translate-x-1/2 -translate-y-1/2 items-center gap-2">
        <span
          className={`h-4 w-4 shrink-0 rounded-full ${nodeColorClasses[node.node_type]} shadow-lg shadow-black`}
        />
        <span
          className={`max-w-[180px] rounded-full bg-slate-900/90 px-3 py-1 text-xs font-semibold ring-1 ring-white/10 ${nodeLabelClasses[node.node_type]}`}
        >
          {node.node_name}
        </span>
      </div>
    </div>
  );
}