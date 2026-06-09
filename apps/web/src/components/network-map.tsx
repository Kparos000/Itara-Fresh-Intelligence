"use client";

import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";

import type { NetworkNode, NetworkNodeType } from "@/data/network";

const nodeColors: Record<NetworkNodeType, string> = {
  warehouse: "#60a5fa",
  store: "#34d399",
  supplier: "#fbbf24",
};

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function NetworkMap({ nodes }: { nodes: NetworkNode[] }) {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);

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

    const bounds = new maplibregl.LngLatBounds();
    const markers: maplibregl.Marker[] = [];

    nodes.forEach((node) => {
      const longitude = node.coordinates.longitude;
      const latitude = node.coordinates.latitude;

      const markerElement = document.createElement("div");
      markerElement.style.width = "18px";
      markerElement.style.height = "18px";
      markerElement.style.borderRadius = "9999px";
      markerElement.style.background = nodeColors[node.node_type];
      markerElement.style.border = "2px solid white";
      markerElement.style.boxShadow = "0 8px 20px rgba(0, 0, 0, 0.35)";
      markerElement.style.cursor = "pointer";

      const popup = new maplibregl.Popup({ offset: 18 }).setHTML(`
        <div style="font-family: system-ui, sans-serif;">
          <strong>${escapeHtml(node.node_name)}</strong>
          <div>${escapeHtml(node.node_type.toUpperCase())}</div>
          <div>${escapeHtml(node.region ?? "Unknown region")}</div>
          <div>${latitude.toFixed(4)}, ${longitude.toFixed(4)}</div>
        </div>
      `);

      const marker = new maplibregl.Marker({ element: markerElement })
        .setLngLat([longitude, latitude])
        .setPopup(popup)
        .addTo(map);

      bounds.extend([longitude, latitude]);
      markers.push(marker);
    });

    if (!bounds.isEmpty()) {
      map.fitBounds(bounds, {
        padding: 70,
        maxZoom: 8.5,
        duration: 0,
      });
    }

    mapRef.current = map;

    return () => {
      markers.forEach((marker) => marker.remove());
      map.remove();
      mapRef.current = null;
    };
  }, [nodes]);

  return (
    <div className="h-[620px] overflow-hidden rounded-2xl border border-slate-800 bg-slate-950">
      <div ref={mapContainerRef} className="h-full w-full" />
    </div>
  );
}