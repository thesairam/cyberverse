<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-lg font-bold text-red-400">Threat Intelligence</h1>
      <div class="ml-auto flex gap-2">
        <select v-model="store.filters.severity" @change="reload"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300">
          <option value="">All Severity</option>
          <option v-for="s in severities" :key="s">{{ s }}</option>
        </select>
        <input v-model="store.filters.search" @keyup.enter="reload" placeholder="Search CVE…"
          class="bg-cyber-700 border border-cyber-600 rounded px-3 py-1.5 text-xs text-gray-300 w-40" />
      </div>
    </div>

    <div class="panel overflow-x-auto">
      <table class="w-full text-xs">
        <thead class="text-gray-500 uppercase border-b border-cyber-600">
          <tr>
            <th class="pb-2 text-left">CVE ID</th>
            <th class="pb-2 text-left">Severity</th>
            <th class="pb-2 text-left">CVSS</th>
            <th class="pb-2 text-left">Title</th>
            <th class="pb-2 text-left">Published</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-cyber-700">
          <tr v-for="t in store.threats" :key="t.id" class="hover:bg-cyber-700/50 transition-colors">
            <td class="py-2 pr-4 font-mono text-cyber-accent whitespace-nowrap">{{ t.indicator_id }}</td>
            <td class="py-2 pr-4"><ThreatBadge :severity="t.severity" /></td>
            <td class="py-2 pr-4 font-mono" :class="cvssColor(t.cvss_score)">{{ t.cvss_score?.toFixed(1) ?? "—" }}</td>
            <td class="py-2 pr-4 text-gray-300 max-w-xs truncate">{{ t.title }}</td>
            <td class="py-2 text-gray-500 whitespace-nowrap">{{ fmtDate(t.published_at) }}</td>
          </tr>
          <tr v-if="!store.threats.length"><td colspan="5" class="py-8 text-center text-gray-600">No threats found</td></tr>
        </tbody>
      </table>
    </div>

    <div class="flex items-center gap-3 justify-center text-xs text-gray-500">
      <button @click="prev" :disabled="store.page===1" class="px-3 py-1 rounded bg-cyber-700 disabled:opacity-40">Prev</button>
      <span>{{ store.page }}</span>
      <button @click="next" :disabled="store.total <= store.page*20" class="px-3 py-1 rounded bg-cyber-700 disabled:opacity-40">Next</button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted } from "vue";
import { format } from "date-fns";
import { useThreatsStore } from "@/stores/threats";
import ThreatBadge from "@/components/ui/ThreatBadge.vue";

const store = useThreatsStore();
const severities = ["CRITICAL","HIGH","MEDIUM","LOW","INFO"];
onMounted(() => store.fetchThreats());
function reload() { store.page = 1; store.fetchThreats(); }
function prev()   { if (store.page > 1) { store.page--; store.fetchThreats(); } }
function next()   { store.page++; store.fetchThreats(); }
function fmtDate(d?: string) { if (!d) return "—"; try { return format(new Date(d), "MM/dd HH:mm"); } catch { return "—"; } }
function cvssColor(s?: number | null) {
  if (!s) return "text-gray-500";
  if (s >= 9) return "text-red-400"; if (s >= 7) return "text-orange-400";
  if (s >= 4) return "text-yellow-400"; return "text-blue-400";
}
</script>
