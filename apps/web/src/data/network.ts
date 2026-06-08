import networkNodesJson from "./network-nodes.json";
import networkSummaryJson from "./network-summary.json";

export type NetworkNodeType = "store" | "warehouse" | "supplier";

export type Coordinates = {
  latitude: number;
  longitude: number;
};

export type NetworkNode = {
  node_id: string;
  node_type: NetworkNodeType;
  node_name: string;
  coordinates: Coordinates;
  region: string | null;
  category_coverage: string[];
  metadata: Record<string, unknown>;
};

export type NetworkSummary = {
  total_nodes: number;
  node_type_counts: {
    store: number;
    supplier: number;
    warehouse: number;
  };
  distance_matrix_entries: number;
  max_estimated_road_distance_km: number;
  max_estimated_drive_minutes: number;
};

export const networkNodes = networkNodesJson as unknown as NetworkNode[];
export const networkSummary = networkSummaryJson as unknown as NetworkSummary;

export const stores = networkNodes.filter((node) => node.node_type === "store");
export const suppliers = networkNodes.filter((node) => node.node_type === "supplier");
export const warehouses = networkNodes.filter((node) => node.node_type === "warehouse");