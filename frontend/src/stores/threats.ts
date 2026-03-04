import { defineStore } from "pinia";
import { ref } from "vue";
import { threatsApi } from "@/services/api";
import type { ThreatIndicator } from "@/types";

export const useThreatsStore = defineStore("threats", () => {
  const threats  = ref<ThreatIndicator[]>([]);
  const critical = ref<ThreatIndicator[]>([]);
  const loading  = ref(false);
  const total    = ref(0);
  const page     = ref(1);
  const filters  = ref({ severity: "", search: "", min_cvss: null as number | null });

  async function fetchThreats(params?: Record<string, unknown>) {
    loading.value = true;
    try {
      const { data } = await threatsApi.list({ page: page.value, page_size: 20, ...filters.value, ...params });
      threats.value = data.items;
      total.value   = data.total;
    } finally { loading.value = false; }
  }

  async function fetchCritical() {
    const { data } = await threatsApi.critical(20);
    critical.value = data;
  }

  return { threats, critical, loading, total, page, filters, fetchThreats, fetchCritical };
});
