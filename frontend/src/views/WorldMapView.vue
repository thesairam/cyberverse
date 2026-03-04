<template>
  <div class="flex flex-col h-full space-y-3">
    <div class="flex items-center gap-4">
      <h1 class="text-lg font-bold text-cyber-accent">Global Intelligence Map</h1>
      <select v-model="eventType" @change="loadMap"
        class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 ml-auto">
        <option value="">All Types</option>
        <option v-for="t in types" :key="t">{{ t }}</option>
      </select>
    </div>
    <div class="flex-1 min-h-[400px]">
      <WorldMap :events="store.mapEvents" />
    </div>
    <p class="text-xs text-gray-600">{{ store.mapEvents.length }} geo-tagged events. Larger circles = higher impact score.</p>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useIntelligenceStore } from "@/stores/intelligence";
import WorldMap from "@/components/map/WorldMap.vue";

const store = useIntelligenceStore();
const types = ["NEWS","ALERT","POLICY"];
const eventType = ref("");
onMounted(() => loadMap());
function loadMap() { store.fetchMapEvents(eventType.value ? { event_type: eventType.value } : {}); }
</script>
