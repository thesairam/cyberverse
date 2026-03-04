<template>
  <div class="space-y-4">
    <div class="flex items-center gap-4">
      <h1 class="text-lg font-bold text-cyber-green">Live Streams</h1>
      <label class="flex items-center gap-2 text-xs text-gray-400 ml-auto cursor-pointer">
        <input type="checkbox" v-model="liveOnly" @change="load" class="accent-cyber-green" />
        Live only
      </label>
    </div>

    <div v-if="!store.streams.length" class="panel text-center py-12 text-gray-600">
      <p>No streams found.</p>
      <p class="text-xs mt-2">YouTube API key required for live stream data.</p>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <a v-for="s in store.streams" :key="s.video_id" :href="s.stream_url" target="_blank" rel="noopener"
         class="panel block hover:border-cyber-green/40 transition-all group">
        <div class="relative">
          <img v-if="s.thumbnail_url" :src="s.thumbnail_url" :alt="s.title"
               class="w-full h-36 object-cover rounded-lg mb-3 group-hover:opacity-90 transition-opacity" />
          <div v-else class="w-full h-36 bg-cyber-700 rounded-lg mb-3 flex items-center justify-center text-gray-600">No Thumbnail</div>
          <span v-if="s.is_live" class="absolute top-2 left-2 badge bg-red-600 text-white animate-pulse-slow">● LIVE</span>
        </div>
        <h3 class="text-sm font-medium text-gray-100 group-hover:text-cyber-green transition-colors line-clamp-2">{{ s.title }}</h3>
        <p class="text-xs text-gray-500 mt-1">{{ s.channel_name }}</p>
        <div class="flex items-center gap-3 mt-2 text-xs text-gray-600">
          <span v-if="s.viewer_count">👁 {{ s.viewer_count.toLocaleString() }}</span>
          <span v-for="t in s.category_tags.slice(0,3)" :key="t" class="bg-cyber-700 px-1.5 py-0.5 rounded">{{ t }}</span>
        </div>
      </a>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useStreamsStore } from "@/stores/streams";
const store = useStreamsStore();
const liveOnly = ref(false);
onMounted(() => load());
function load() { store.fetchStreams(liveOnly.value); }
</script>
