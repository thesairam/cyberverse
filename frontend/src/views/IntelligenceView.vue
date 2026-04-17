<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-lg font-bold text-cyber-accent">Intelligence Feed</h1>
      <span class="text-xs text-gray-500">{{ store.total }} events from {{ store.sources.length }} sources</span>
      <div class="ml-auto flex flex-wrap gap-2">
        <select v-model="store.filters.event_type" @change="reload"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300">
          <option value="">All Types</option>
          <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
        </select>
        <select v-model="store.filters.source_name" @change="reload"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 max-w-[180px]">
          <option value="">All Sources</option>
          <option v-for="s in store.sources" :key="s.name" :value="s.name">{{ s.name }} ({{ s.count }})</option>
        </select>
        <input v-model="store.filters.search" @keyup.enter="reload" placeholder="Search…"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 w-40" />
        <input v-model.number="store.filters.min_impact" @change="reload" type="number" placeholder="Min impact"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 w-28" />
      </div>
    </div>

    <!-- Active category tag filters -->
    <div v-if="activeTag" class="flex items-center gap-2">
      <span class="text-xs text-gray-500">Filtered by tag:</span>
      <span class="text-xs px-2 py-0.5 bg-cyber-accent/20 text-cyber-accent rounded-full">{{ activeTag }}</span>
      <button @click="clearTag" class="text-xs text-gray-500 hover:text-red-400">&times;</button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
      <EventCard v-for="ev in store.events" :key="ev.id" :event="ev" @tag-click="filterByTag" />
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
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useIntelligenceStore } from "@/stores/intelligence";
import EventCard from "@/components/ui/EventCard.vue";

const store = useIntelligenceStore();
const route = useRoute();
const types = ["NEWS","ALERT","POLICY","FINANCIAL","VIDEO","CERTIFICATION","STARTUP","PRODUCT"];
const activeTag = ref("");

onMounted(() => {
  if (route.query.search) store.filters.search = String(route.query.search);
  store.fetchSources();
  store.fetchEvents();
});
watch(() => route.query.search, v => { if (v) { store.filters.search = String(v); reload(); } });

function reload() { store.page = 1; store.fetchEvents(); }
function prev()   { if (store.page > 1) { store.page--; store.fetchEvents(); } }
function next()   { if (store.page < store.totalPages) { store.page++; store.fetchEvents(); } }

function filterByTag(tag: string) {
  activeTag.value = tag;
  store.filters.search = tag;
  reload();
}
function clearTag() {
  activeTag.value = "";
  store.filters.search = "";
  reload();
}
</script>
