<template>
  <div class="space-y-4">
    <h1 class="text-lg font-bold text-purple-400">Certifications & Standards</h1>

    <div class="flex flex-wrap gap-2">
      <button @click="activeBody = ''" :class="btnClass('')">All</button>
      <button v-for="b in bodies" :key="b" @click="filterBody(b)" :class="btnClass(b)">{{ b }}</button>
    </div>

    <div class="space-y-2">
      <div v-for="c in store.items" :key="c.id"
           class="panel flex items-start gap-4 hover:border-purple-400/40 transition-all">
        <div class="bg-purple-500/20 text-purple-400 px-2 py-1 rounded text-xs font-bold whitespace-nowrap">{{ c.body_name }}</div>
        <div class="flex-1 min-w-0">
          <a :href="c.source_url ?? undefined" target="_blank" class="text-sm font-medium text-gray-100 hover:text-purple-400 transition-colors line-clamp-2">
            {{ c.title }}
          </a>
          <div class="flex items-center gap-3 mt-1 text-xs text-gray-500">
            <span v-if="c.region">🌍 {{ c.region }}</span>
            <span v-if="c.update_type" class="badge bg-gray-700 text-gray-300">{{ c.update_type }}</span>
            <span v-if="c.published_at">{{ fmtDate(c.published_at) }}</span>
          </div>
        </div>
      </div>
      <p v-if="!store.items.length" class="text-center text-gray-600 py-8">No certification updates found</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { format } from "date-fns";
import { certificationsApi } from "@/services/api";
import type { CertificationUpdate, PaginatedResponse } from "@/types";

const bodies    = ref<string[]>([]);
const activeBody = ref("");
const store = reactive({ items: [] as CertificationUpdate[] });

onMounted(async () => {
  const [certRes, bodiesRes] = await Promise.all([
    certificationsApi.list({ page_size: 50 }),
    certificationsApi.bodies(),
  ]);
  store.items = certRes.data.items;
  bodies.value = bodiesRes.data.bodies;
});

async function filterBody(b: string) {
  activeBody.value = b;
  const { data } = await certificationsApi.list({ body_name: b, page_size: 50 });
  store.items = data.items;
}

function btnClass(b: string) {
  return ["px-3 py-1 text-xs rounded border transition-colors",
    activeBody.value === b
      ? "border-purple-400 text-purple-400 bg-purple-400/10"
      : "border-cyber-600 text-gray-400 hover:text-gray-200"].join(" ");
}

function fmtDate(d: string) { try { return format(new Date(d), "MMM d, yyyy"); } catch { return "—"; } }
</script>
