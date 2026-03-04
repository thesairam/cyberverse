import { defineStore } from "pinia";
import { ref } from "vue";
import { financialApi } from "@/services/api";
import type { FinancialSnapshot } from "@/types";

export const useFinancialStore = defineStore("financial", () => {
  const snapshots     = ref<FinancialSnapshot[]>([]);
  const gainers       = ref<FinancialSnapshot[]>([]);
  const losers        = ref<FinancialSnapshot[]>([]);
  const tickerHistory = ref<Record<string, FinancialSnapshot[]>>({});
  const loading       = ref(false);

  async function fetchSnapshots(sector?: string) {
    loading.value = true;
    try { const { data } = await financialApi.list(sector); snapshots.value = data; }
    finally { loading.value = false; }
  }

  async function fetchMovers() {
    const { data } = await financialApi.movers();
    gainers.value = data.gainers;
    losers.value  = data.losers;
  }

  async function fetchHistory(ticker: string) {
    const { data } = await financialApi.history(ticker);
    tickerHistory.value[ticker] = data;
  }

  return { snapshots, gainers, losers, tickerHistory, loading, fetchSnapshots, fetchMovers, fetchHistory };
});
