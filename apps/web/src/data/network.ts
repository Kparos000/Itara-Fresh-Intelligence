export type NetworkNodeType = "store" | "warehouse" | "supplier";

export type NetworkNode = {
  id: string;
  name: string;
  type: NetworkNodeType;
  region: string;
  latitude: number;
  longitude: number;
  description: string;
};

export const networkNodes: NetworkNode[] = [
  {
    id: "warehouse_001",
    name: "Itara Central Fresh Distribution Centre",
    type: "warehouse",
    region: "Central Distribution",
    latitude: 43.7418,
    longitude: -79.5294,
    description: "Main network warehouse for supplier receiving and store replenishment.",
  },
  {
    id: "store_001",
    name: "King West Fresh",
    type: "store",
    region: "Old Toronto",
    latitude: 43.6436,
    longitude: -79.4023,
    description: "High prepared-foods demand store serving young professionals.",
  },
  {
    id: "store_004",
    name: "Yonge Sheppard Fresh",
    type: "store",
    region: "North York",
    latitude: 43.7615,
    longitude: -79.4111,
    description: "Transit-hub urban store with strong weekday demand.",
  },
  {
    id: "store_006",
    name: "Scarborough Town Centre Fresh",
    type: "store",
    region: "Scarborough",
    latitude: 43.7764,
    longitude: -79.2579,
    description: "High-volume suburban mall anchor store.",
  },
  {
    id: "store_014",
    name: "Square One Fresh",
    type: "store",
    region: "Mississauga",
    latitude: 43.5934,
    longitude: -79.6399,
    description: "Flagship suburban family store with high volume.",
  },
  {
    id: "supplier_001",
    name: "Ontario Greenhouse Produce Co.",
    type: "supplier",
    region: "Leamington Produce Hub",
    latitude: 42.0531,
    longitude: -82.5998,
    description: "Primary produce supplier shipping bulk inventory to the warehouse.",
  },
  {
    id: "supplier_003",
    name: "Golden Horseshoe Dairy",
    type: "supplier",
    region: "Guelph Dairy Cold Hub",
    latitude: 43.5448,
    longitude: -80.2482,
    description: "Dairy supplier with frequent cold-chain delivery schedule.",
  },
];

export const networkSummary = {
  stores: 15,
  suppliers: 10,
  warehouses: 1,
  skus: 500,
  policies: 5,
  distanceMatrixEntries: 650,
};