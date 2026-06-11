"use client";

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";

import type { NetworkNode, NetworkNodeType } from "@/data/network";

const nodeColors: Record<NetworkNodeType, string> = {
  warehouse: "#60a5fa",
  store: "#34d399",
  supplier: "#fbbf24",
};

function nodeTypeLabel(nodeType: NetworkNodeType) {
  if (nodeType === "warehouse") {
    return "Warehouse";
  }

  if (nodeType === "supplier") {
    return "Supplier";
  }

  return "Store";
}

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function popupHtml(node: NetworkNode) {
  const categories =
    node.category_coverage.length > 0
      ? node.category_coverage.join(", ")
      : "No category coverage";

  return `
    <div style="min-width: 240px; color: #0f172a; font-family: system-ui, sans-serif;">
      <div style="font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #475569;">
        ${escapeHtml(nodeTypeLabel(node.node_type))}
      </div>

      <div style="margin-top: 6px; font-size: 18px; font-weight: 800; line-height: 1.25; color: #020617;">
        ${escapeHtml(node.node_name)}
      </div>

      <div style="margin-top: 10px; font-size: 13px; color: #334155;">
        <strong>Region:</strong> ${escapeHtml(node.region ?? "Unknown region")}
      </div>

      <div style="margin-top: 4px; font-size: 13px; color: #334155;">
        <strong>Coordinates:</strong> ${node.coordinates.latitude.toFixed(4)}, ${node.coordinates.longitude.toFixed(4)}
      </div>

      <div style="margin-top: 4px; font-size: 13px; color: #334155;">
        <strong>Categories:</strong> ${escapeHtml(categories)}
      </div>

      <div style="margin-top: 10px; border-radius: 9999px; background: #f1f5f9; padding: 5px 9px; display: inline-block; font-size: 12px; font-weight: 700; color: #0f172a;">
        ${escapeHtml(node.node_id)}
      </div>
    </div>
  `;
}

function warehouseToStoreRouteGeoJson(nodes: NetworkNode[]) {
  const warehouse = nodes.find((node) => node.node_type === "warehouse");
  const stores = nodes.filter((node) => node.node_type === "store");

  if (!warehouse) {
    return {
      type: "FeatureCollection" as const,
      features: [],
    };
  }

  return {
    type: "FeatureCollection" as const,
    features: stores.map((store) => ({
      type: "Feature" as const,
      properties: {
        route_id: `${warehouse.node_id}_to_${store.node_id}`,
        source: warehouse.node_id,
        target: store.node_id,
        route_type: "warehouse_to_store_replenishment",
      },
      geometry: {
        type: "LineString" as const,
        coordinates: [
          [warehouse.coordinates.longitude, warehouse.coordinates.latitude],
          [store.coordinates.longitude, store.coordinates.latitude],
        ],
      },
    })),
  };
}

export function NetworkMap({
  nodes,
  selectedNodeId,
  showWarehouseRoutes,
  onNodeSelect,
}: {
  nodes: NetworkNode[];
  selectedNodeId: string | null;
  showWarehouseRoutes: boolean;
  onNodeSelect: (nodeId: string) => void;
}) {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<Map<string, maplibregl.Marker>>(new Map());

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) {
      return;
    }

    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors",
          },
        },
        layers: [
          {
            id: "osm",
            type: "raster",
            source: "osm",
          },
        ],
      },
      center: [-79.4, 43.7],
      zoom: 8,
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    map.on("load", () => {
      map.addSource("warehouse-routes", {
        type: "geojson",
        data: warehouseToStoreRouteGeoJson(nodes),
      });

      map.addLayer({
        id: "warehouse-routes-glow",
        type: "line",
        source: "warehouse-routes",
        layout: {
          visibility: showWarehouseRoutes ? "visible" : "none",
          "line-cap": "round",
          "line-join": "round",
        },
        paint: {
          "line-color": "#93c5fd",
          "line-width": 9,
          "line-opacity": 0.35,
        },
      });

      map.addLayer({
        id: "warehouse-routes",
        type: "line",
        source: "warehouse-routes",
        layout: {
          visibility: showWarehouseRoutes ? "visible" : "none",
          "line-cap": "round",
          "line-join": "round",
        },
        paint: {
          "line-color": "#2563eb",
          "line-width": 4,
          "line-opacity": 0.9,
          "line-dasharray": [2, 1],
        },
      });
    });

    const bounds = new maplibregl.LngLatBounds();
    const markers = new Map<string, maplibregl.Marker>();

    nodes.forEach((node) => {
      const longitude = node.coordinates.longitude;
      const latitude = node.coordinates.latitude;

      const markerElement = document.createElement("button");
      markerElement.type = "button";
      markerElement.setAttribute("aria-label", `Select ${node.node_name}`);
      markerElement.style.width = "18px";
      markerElement.style.height = "18px";
      markerElement.style.borderRadius = "9999px";
      markerElement.style.background = nodeColors[node.node_type];
      markerElement.style.border = "2px solid white";
      markerElement.style.boxShadow = "0 8px 20px rgba(0, 0, 0, 0.35)";
      markerElement.style.cursor = "pointer";

      markerElement.addEventListener("click", () => {
        onNodeSelect(node.node_id);
      });

      const popup = new maplibregl.Popup({ offset: 18 }).setHTML(popupHtml(node));

      const marker = new maplibregl.Marker({ element: markerElement })
        .setLngLat([longitude, latitude])
        .setPopup(popup)
        .addTo(map);

      bounds.extend([longitude, latitude]);
      markers.set(node.node_id, marker);
    });

    if (!bounds.isEmpty()) {
      map.fitBounds(bounds, {
        padding: 70,
        maxZoom: 8.5,
        duration: 0,
      });
    }

    markersRef.current = markers;
    mapRef.current = map;

    return () => {
      markers.forEach((marker) => marker.remove());
      markers.clear();
      map.remove();
      mapRef.current = null;
    };
  }, [nodes, onNodeSelect, showWarehouseRoutes]);

  useEffect(() => {
    const map = mapRef.current;

    if (!map) {
      return;
    }

    const visibility = showWarehouseRoutes ? "visible" : "none";

    if (map.getLayer("warehouse-routes")) {
      map.setLayoutProperty("warehouse-routes", "visibility", visibility);
    }

    if (map.getLayer("warehouse-routes-glow")) {
      map.setLayoutProperty("warehouse-routes-glow", "visibility", visibility);
    }
  }, [showWarehouseRoutes]);

  useEffect(() => {
    if (!selectedNodeId) {
      return;
    }

    const selectedNode = nodes.find((node) => node.node_id === selectedNodeId);
    const marker = markersRef.current.get(selectedNodeId);

    if (!selectedNode || !marker || !mapRef.current) {
      return;
    }

    mapRef.current.flyTo({
      center: [selectedNode.coordinates.longitude, selectedNode.coordinates.latitude],
      zoom: 10,
      essential: true,
    });

    marker.togglePopup();
  }, [nodes, selectedNodeId]);

  return (
    <div className="h-[620px] overflow-hidden rounded-2xl border border-slate-800 bg-slate-950">
      <div ref={mapContainerRef} className="h-full w-full" />
    </div>
  );
}