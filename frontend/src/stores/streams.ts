import { defineStore } from "pinia";
import { ref } from "vue";
import { streamsApi } from "@/services/api";
import type { LiveStream } from "@/types";

export const useStreamsStore = defineStore("streams", () => {
  const streams = ref<LiveStream[]>([]);
  const loading = ref(false);

  async function fetchStreams(liveOnly = false) {
    loading.value = true;
    try { const { data } = await streamsApi.list(liveOnly); streams.value = data; }
    finally { loading.value = false; }
  }

  return { streams, loading, fetchStreams };
});
