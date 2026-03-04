<template>
  <nav class="w-16 lg:w-56 bg-cyber-800 border-r border-cyber-600 flex flex-col flex-shrink-0 h-full">
    <!-- Logo -->
    <div class="flex items-center gap-3 p-4 border-b border-cyber-600">
      <div class="w-8 h-8 rounded bg-cyber-accent/20 flex items-center justify-center relative">
        <Shield class="w-5 h-5 text-cyber-accent" />
        <span class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-cyber-green rounded-full animate-pulse-slow" />
      </div>
      <span class="hidden lg:block text-xs font-bold text-cyber-accent tracking-widest uppercase">CyberVerse</span>
    </div>

    <!-- Nav Items -->
    <div class="flex-1 py-4 space-y-1 px-2">
      <RouterLink
        v-for="item in navItems" :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group"
        :class="$route.path === item.to
          ? 'bg-cyber-accent/10 text-cyber-accent border border-cyber-accent/30'
          : 'text-gray-400 hover:text-gray-100 hover:bg-cyber-700'"
      >
        <component :is="item.icon" class="w-4 h-4 flex-shrink-0" />
        <span class="hidden lg:block text-xs font-medium">{{ item.label }}</span>
      </RouterLink>
    </div>

    <div class="p-4 border-t border-cyber-600 hidden lg:block">
      <p class="text-xs text-gray-500">v1.0.0</p>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { LayoutDashboard, Newspaper, ShieldAlert, Globe, TrendingUp, Radio, Award } from "lucide-vue-next";
import { Shield } from "lucide-vue-next";
const navItems = [
  { to: "/",               icon: LayoutDashboard, label: "Dashboard" },
  { to: "/intelligence",   icon: Newspaper,       label: "Intelligence" },
  { to: "/threats",        icon: ShieldAlert,     label: "Threat Intel" },
  { to: "/map",            icon: Globe,           label: "World Map" },
  { to: "/financial",      icon: TrendingUp,      label: "Financial" },
  { to: "/streams",        icon: Radio,           label: "Live Streams" },
  { to: "/certifications", icon: Award,           label: "Certifications" },
];
</script>
