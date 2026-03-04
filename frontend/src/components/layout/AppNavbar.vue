<template>
  <header class="h-14 bg-cyber-800 border-b border-cyber-600 flex items-center px-4 gap-4">
    <div class="flex-1 max-w-md">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
        <input
          v-model="searchQuery"
          @keyup.enter="doSearch"
          type="text"
          placeholder="Search intelligence..."
          class="w-full bg-cyber-700 border border-cyber-600 rounded-lg pl-9 pr-4 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyber-accent/60"
        />
      </div>
    </div>

    <div class="flex items-center gap-3 ml-auto">
      <button @click="refresh" class="p-2 rounded-lg hover:bg-cyber-700 text-gray-400 hover:text-cyber-accent transition-colors" title="Refresh">
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': refreshing }" />
      </button>
      <div class="text-xs text-gray-500 font-mono hidden sm:block">{{ utcClock }}</div>
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 bg-cyber-green rounded-full animate-pulse-slow" />
        <span class="text-xs text-cyber-green hidden sm:block">LIVE</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { Search, RefreshCw } from "lucide-vue-next";

const router = useRouter();
const searchQuery = ref("");
const refreshing  = ref(false);
const utcClock    = ref("");

let clockInterval: ReturnType<typeof setInterval>;

onMounted(() => {
  clockInterval = setInterval(() => {
    utcClock.value = new Date().toUTCString().slice(17, 25) + " UTC";
  }, 1000);
});
onUnmounted(() => clearInterval(clockInterval));

function doSearch() {
  if (searchQuery.value.trim())
    router.push({ path: "/intelligence", query: { search: searchQuery.value.trim() } });
}

async function refresh() {
  refreshing.value = true;
  window.location.reload();
}
</script>
