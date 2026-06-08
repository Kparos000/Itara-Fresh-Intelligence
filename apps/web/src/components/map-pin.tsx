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
  className,
}: {
  node: NetworkNode;
  className: string;
}) {
  return (
    <div className={`absolute ${className}`}>
      <div className="flex items-center gap-2">
        <span
          className={`h-4 w-4 rounded-full ${nodeColorClasses[node.node_type]} shadow-lg shadow-black`}
        />
        <span
          className={`rounded-full bg-slate-900/90 px-3 py-1 text-xs font-semibold ring-1 ring-white/10 ${nodeLabelClasses[node.node_type]}`}
        >
          {node.node_name}
        </span>
      </div>
    </div>
  );
}