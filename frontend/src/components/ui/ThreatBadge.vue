<template>
  <span class="badge font-mono" :class="colorClass">
    {{ severity }}{{ cvss !== undefined ? ` ${cvss.toFixed(1)}` : "" }}
  </span>
</template>
<script setup lang="ts">
import { computed } from "vue";
const props = defineProps<{ severity?: string; cvss?: number }>();
const colorClass = computed(() => ({
  CRITICAL: "bg-red-600/30 text-red-300 border border-red-500/40",
  HIGH:     "bg-orange-500/30 text-orange-300 border border-orange-500/40",
  MEDIUM:   "bg-yellow-500/20 text-yellow-300 border border-yellow-500/30",
  LOW:      "bg-blue-500/20 text-blue-300 border border-blue-500/30",
  INFO:     "bg-gray-500/20 text-gray-400",
}[props.severity?.toUpperCase() ?? "INFO"] ?? "bg-gray-500/20 text-gray-400"));
</script>
