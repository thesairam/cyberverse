<template>
  <div ref="mapEl" class="w-full h-full rounded-xl overflow-hidden" />
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type { IntelligenceEvent } from "@/types";

const props = defineProps<{ events: IntelligenceEvent[] }>();
const mapEl = ref<HTMLElement | null>(null);
let map: L.Map | null = null;
let markersLayer: L.LayerGroup | null = null;

function impactColor(score: number) {
  if (score >= 8) return "#ff4560";
  if (score >= 5) return "#ffd700";
  if (score >= 3) return "#00d8ff";
  return "#4ade80";
}

function renderMarkers() {
  if (!map) return;
  markersLayer?.clearLayers();
  props.events.forEach(ev => {
    if (ev.latitude == null || ev.longitude == null) return;
    L.circleMarker([ev.latitude, ev.longitude], {
      radius: 6 + ev.impact_score,
      color: impactColor(ev.impact_score),
      fillColor: impactColor(ev.impact_score),
      fillOpacity: 0.75,
      weight: 1,
    })
    .bindPopup(`<b>${ev.title}</b><br><small>${ev.source_name} · ${ev.country ?? ""}</small>`)
    .addTo(markersLayer!);
  });
}

onMounted(() => {
  if (!mapEl.value) return;
  map = L.map(mapEl.value, { center: [20, 0], zoom: 2, zoomControl: true });
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "© CartoDB",
    maxZoom: 18,
  }).addTo(map);
  markersLayer = L.layerGroup().addTo(map);
  renderMarkers();
});

watch(() => props.events, renderMarkers, { deep: true });
</script>
