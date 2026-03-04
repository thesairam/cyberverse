<template>
  <div class="space-y-5">
    <h1 class="text-lg font-bold text-cyber-accent tracking-wide">Dashboard</h1>

    <!-- KPI Row -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard label="Total Events"   :value="stats?.total ?? 0"            :icon="Newspaper"    iconBg="bg-blue-500/10"   iconColor="text-blue-400" />
      <StatCard label="Threat Alerts"  :value="threatStore.critical.length"  :icon="ShieldAlert"  iconBg="bg-red-500/10"    iconColor="text-red-400" />
      <StatCard label="Tracked Stocks" :value="finStore.snapshots.length"    :icon="TrendingUp"   iconBg="bg-yellow-500/10" iconColor="text-yellow-400" />
      <StatCard label="Live Streams"   :value="streamStore.streams.filter(s=>s.is_live).length" :icon="Radio" iconBg="bg-green-500/10" iconColor="text-cyber-green" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Top Events -->
      <div class="lg:col-span-2 space-y-3">
        <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Top Impact Events</h2>
        <div v-if="intelStore.loading" class="text-gray-500 text-sm">Loading…</div>
        <div v-else class="grid sm:grid-cols-2 gap-3">
          <EventCard v-for="ev in intelStore.topEvents.slice(0,6)" :key="ev.id" :event="ev" />
        </div>
      </div>

      <!-- Right column -->
      <div class="space-y-4">
        <!-- Critical CVEs -->
        <div class="panel space-y-2">
          <h2 class="text-sm font-semibold text-red-400 uppercase tracking-wider">Critical CVEs</h2>
          <div v-for="t in threatStore.critical.slice(0,5)" :key="t.id" class="flex items-start gap-2 text-xs">
            <ThreatBadge :severity="t.severity" :cvss="t.cvss_score ?? undefined" />
            <span class="text-gray-300 line-clamp-2">{{ t.indicator_id }}: {{ t.title.slice(0,60) }}</span>
          </div>
          <p v-if="!threatStore.critical.length" class="text-gray-600 text-xs">No critical threats found</p>
        </div>

        <!-- Market movers -->
        <div class="panel">
          <h2 class="text-sm font-semibold text-yellow-400 uppercase tracking-wider mb-2">Market Movers</h2>
          <div class="space-y-1">
            <div v-for="s in [...finStore.gainers.slice(0,3), ...finStore.losers.slice(0,2)]" :key="s.ticker"
                 class="flex items-center justify-between text-xs">
              <span class="font-mono font-bold">{{ s.ticker }}</span>
              <span :class="(s.change_pct ?? 0) >= 0 ? 'text-cyber-green' : 'text-cyber-red'">
                {{ (s.change_pct ?? 0) >= 0 ? "+" : "" }}{{ (s.change_pct ?? 0).toFixed(2) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { Newspaper, ShieldAlert, TrendingUp, Radio } from "lucide-vue-next";
import { useIntelligenceStore } from "@/stores/intelligence";
import { useFinancialStore }    from "@/stores/financial";
import { useThreatsStore }      from "@/stores/threats";
import { useStreamsStore }      from "@/stores/streams";
import StatCard   from "@/components/ui/StatCard.vue";
import EventCard  from "@/components/ui/EventCard.vue";
import ThreatBadge from "@/components/ui/ThreatBadge.vue";

const intelStore  = useIntelligenceStore();
const finStore    = useFinancialStore();
const threatStore = useThreatsStore();
const streamStore = useStreamsStore();
const stats       = intelStore.stats;

onMounted(async () => {
  await Promise.all([
    intelStore.fetchTopEvents(10),
    intelStore.fetchStats(),
    finStore.fetchSnapshots(),
    finStore.fetchMovers(),
    threatStore.fetchCritical(),
    streamStore.fetchStreams(),
  ]);
});
</script>
