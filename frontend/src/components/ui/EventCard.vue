<template>
  <a :href="event.source_url" target="_blank" rel="noopener"
     class="panel block hover:border-cyber-accent/40 hover:glow-accent transition-all cursor-pointer group">
    <div class="flex items-start justify-between gap-2 mb-2">
      <EventTypeBadge :type="event.event_type" />
      <div class="flex items-center gap-1 flex-shrink-0">
        <span class="text-xs font-bold"
          :class="event.impact_score >= 7 ? 'text-red-400' : event.impact_score >= 4 ? 'text-yellow-400' : 'text-gray-500'">
          ⚡ {{ event.impact_score.toFixed(1) }}
        </span>
      </div>
    </div>
    <h3 class="text-sm font-medium text-gray-100 group-hover:text-cyber-accent transition-colors line-clamp-2 mb-2">
      {{ event.title }}
    </h3>
    <div class="flex items-center gap-3 text-xs text-gray-500">
      <span>{{ event.source_name }}</span>
      <span v-if="event.country">🌍 {{ event.country }}</span>
      <span class="ml-auto">{{ formatDate(event.published_at) }}</span>
    </div>
    <div class="flex flex-wrap gap-1 mt-2">
      <span v-for="tag in event.category_tags.slice(0,4)" :key="tag"
        class="text-xs px-1.5 py-0.5 bg-cyber-700 text-gray-400 rounded">{{ tag }}</span>
    </div>
  </a>
</template>
<script setup lang="ts">
import { formatDistanceToNow } from "date-fns";
import EventTypeBadge from "@/components/ui/EventTypeBadge.vue";
import type { IntelligenceEvent } from "@/types";
defineProps<{ event: IntelligenceEvent }>();
function formatDate(d?: string) {
  if (!d) return "—";
  try { return formatDistanceToNow(new Date(d), { addSuffix: true }); }
  catch { return "—"; }
}
</script>
