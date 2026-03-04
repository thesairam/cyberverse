<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-lg font-bold text-cyber-accent">Intelligence Feed</h1>
      <div class="ml-auto flex flex-wrap gap-2">
        <select v-model="store.filters.event_type" @change="reload"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300">
          <option value="">All Types</option>
          <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
        </select>
        <input v-model="store.filters.search" @keyup.enter="reload" placeholder="Search…"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 w-40" />
        <input v-model.number="store.filters.min_impact" @change="reload" type="number" placeholder="Min impact"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 w-28" />
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
      <EventCard v-for="ev in store.events" :key="ev.id" :event="ev" />
    </div>

    <div class="flex items-center gap-3 justify-center text-xs text-gray-500">
      <button @click="prev" :disabled="store.page === 1"
        class="px-3 py-1 rounded bg-cyber-700 disabled:opacity-40">Prev</button>
      <span>{{ store.page }} / {{ store.totalPages }}</span>
      <button @click="next" :disabled="store.page >= store.totalPages"
        class="px-3 py-1 rounded bg-cyber-700 disabled:opacity-40">Next</button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useIntelligenceStore } from "@/stores/intelligence";
import EventCard from "@/components/ui/EventCard.vue";

const store = useIntelligenceStore();
const route = useRoute();
const types = ["NEWS","ALERT","POLICY","FINANCIAL","VIDEO","CERTIFICATION","STARTUP","PRODUCT"];

onMounted(() => {
  if (route.query.search) store.filters.search = String(route.query.search);
  store.fetchEvents();
});
watch(() => route.query.search, v => { if (v) { store.filters.search = String(v); reload(); } });

function reload() { store.page = 1; store.fetchEvents(); }
function prev()   { if (store.page > 1) { store.page--; store.fetchEvents(); } }
function next()   { if (store.page < store.totalPages) { store.page++; store.fetchEvents(); } }
</script>
