<template>
  <div class="panel flex items-start gap-4">
    <div class="p-2 rounded-lg" :class="iconBg">
      <component :is="icon" class="w-5 h-5" :class="iconColor" />
    </div>
    <div class="flex-1 min-w-0">
      <p class="text-xs text-gray-500 uppercase tracking-wider">{{ label }}</p>
      <p class="text-2xl font-bold mt-0.5" :class="valueColor">{{ formattedValue }}</p>
      <p v-if="delta !== undefined" class="text-xs mt-1" :class="deltaColor">
        <TrendingUp v-if="delta >= 0" class="inline w-3 h-3 mr-0.5" />
        <TrendingDown v-else class="inline w-3 h-3 mr-0.5" />
        {{ Math.abs(delta).toFixed(1) }}%
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { TrendingUp, TrendingDown } from "lucide-vue-next";
const props = defineProps<{
  label: string; value: number | string; icon: unknown;
  delta?: number; iconBg?: string; iconColor?: string; valueColor?: string;
}>();
const formattedValue = computed(() =>
  typeof props.value === "number" && props.value > 9999
    ? (props.value / 1000).toFixed(1) + "k"
    : props.value
);
const deltaColor = computed(() => (props.delta ?? 0) >= 0 ? "text-cyber-green" : "text-cyber-red");
</script>
