<template>
  <Line :data="chartData" :options="chartOptions" />
</template>
<script setup lang="ts">
import { computed } from "vue";
import { Line } from "vue-chartjs";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const props = defineProps<{
  labels: string[];
  datasets: { label: string; data: number[]; color?: string }[];
}>();

const chartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets.map((d, i) => ({
    label: d.label,
    data: d.data,
    borderColor: d.color ?? ["#00d8ff","#00ff9d","#ff4560","#ffd700"][i % 4],
    backgroundColor: (d.color ?? "#00d8ff") + "22",
    fill: true,
    tension: 0.4,
    pointRadius: 2,
  })),
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: "#94a3b8", font: { size: 11 } } } },
  scales: {
    x: { ticks: { color: "#64748b" }, grid: { color: "#1a2235" } },
    y: { ticks: { color: "#64748b" }, grid: { color: "#1a2235" } },
  },
};
</script>
