<template>
  <span class="badge" :class="colorClass">{{ type }}</span>
</template>
<script setup lang="ts">
import { computed } from "vue";
const props = defineProps<{ type: string }>();
const colorClass = computed(() => ({
  NEWS:          "bg-blue-500/20 text-blue-400",
  ALERT:         "bg-red-500/20 text-red-400",
  POLICY:        "bg-purple-500/20 text-purple-400",
  FINANCIAL:     "bg-yellow-500/20 text-yellow-400",
  VIDEO:         "bg-pink-500/20 text-pink-400",
  CERTIFICATION: "bg-green-500/20 text-green-400",
  STARTUP:       "bg-orange-500/20 text-orange-400",
  PRODUCT:       "bg-teal-500/20 text-teal-400",
}[props.type.toUpperCase()] ?? "bg-gray-500/20 text-gray-400"));
</script>
