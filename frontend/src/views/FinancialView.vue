<template>
  <div class="space-y-4">
    <div class="flex items-center gap-4">
      <h1 class="text-lg font-bold text-yellow-400">Financial Intelligence</h1>
      <div class="ml-auto flex gap-2">
        <button v-for="s in sectors" :key="s" @click="filter(s)"
          :class="['px-3 py-1.5 text-xs rounded border transition-colors', activeSector===s ? 'border-yellow-400 text-yellow-400 bg-yellow-400/10' : 'border-cyber-600 text-gray-400 hover:text-gray-200']">
          {{ s || "All" }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-3">
      <div v-for="s in store.snapshots" :key="s.ticker"
           class="panel hover:border-yellow-400/40 transition-all cursor-pointer" @click="loadChart(s.ticker)">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-xs text-gray-500 uppercase">{{ s.ticker }}</p>
            <p class="text-lg font-bold font-mono">${{ s.price?.toFixed(2) ?? "—" }}</p>
          </div>
          <span class="badge text-xs font-mono" :class="(s.change_pct??0)>=0 ? 'bg-green-500/20 text-cyber-green' : 'bg-red-500/20 text-cyber-red'">
            {{ (s.change_pct??0) >= 0 ? "+" : "" }}{{ (s.change_pct??0).toFixed(2) }}%
          </span>
        </div>
        <p class="text-xs text-gray-600 truncate mt-1">{{ s.company_name }}</p>
        <p class="text-xs text-gray-600 mt-0.5">MCap: ${{ fmtMcap(s.market_cap) }}</p>
      </div>
    </div>

    <div v-if="chartTicker" class="panel h-64">
      <h3 class="text-sm text-gray-400 mb-2">{{ chartTicker }} price history</h3>
      <TrendChart :labels="chartLabels" :datasets="chartDatasets" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { format } from "date-fns";
import { useFinancialStore } from "@/stores/financial";
import TrendChart from "@/components/charts/TrendChart.vue";

const store = useFinancialStore();
const sectors = ["", "cybersecurity", "ai"];
const activeSector = ref("");
const chartTicker = ref("");

const chartLabels = computed(() =>
  (store.tickerHistory[chartTicker.value] ?? []).map(s => format(new Date(s.snapshot_at!), "MM/dd HH:mm")).reverse()
);
const chartDatasets = computed(() => [{
  label: chartTicker.value,
  data: (store.tickerHistory[chartTicker.value] ?? []).map(s => s.price ?? 0).reverse(),
}]);

onMounted(() => store.fetchSnapshots());
function filter(s: string) { activeSector.value = s; store.fetchSnapshots(s || undefined); }
function loadChart(ticker: string) { chartTicker.value = ticker; store.fetchHistory(ticker); }
function fmtMcap(v?: number | null) {
  if (!v) return "—";
  if (v >= 1e12) return (v/1e12).toFixed(2)+"T";
  if (v >= 1e9)  return (v/1e9).toFixed(2)+"B";
  return (v/1e6).toFixed(0)+"M";
}
</script>
