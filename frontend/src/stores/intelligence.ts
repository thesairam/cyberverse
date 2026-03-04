import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { intelligenceApi } from "@/services/api";
import type { IntelligenceEvent, DashboardStats } from "@/types";

export const useIntelligenceStore = defineStore("intelligence", () => {
  const events     = ref<IntelligenceEvent[]>([]);
  const topEvents  = ref<IntelligenceEvent[]>([]);
  const mapEvents  = ref<IntelligenceEvent[]>([]);
  const stats      = ref<DashboardStats | null>(null);
  const loading    = ref(false);
  const total      = ref(0);
  const page       = ref(1);
  const filters    = ref({ event_type: "", country: "", search: "", min_impact: null as number | null });

  async function fetchEvents(params?: Record<string, unknown>) {
    loading.value = true;
    try {
      const { data } = await intelligenceApi.list({ page: page.value, page_size: 20, ...filters.value, ...params });
      events.value = data.items;
      total.value  = data.total;
    } finally { loading.value = false; }
  }

  async function fetchTopEvents(n = 10) {
    const { data } = await intelligenceApi.top(n);
    topEvents.value = data;
  }

  async function fetchMapEvents(params?: Record<string, unknown>) {
    const { data } = await intelligenceApi.map(params);
    mapEvents.value = data;
  }

  async function fetchStats() {
    const { data } = await intelligenceApi.stats();
    stats.value = data;
  }

  const totalPages = computed(() => Math.ceil(total.value / 20));

  return { events, topEvents, mapEvents, stats, loading, total, page, filters, totalPages, fetchEvents, fetchTopEvents, fetchMapEvents, fetchStats };
});
