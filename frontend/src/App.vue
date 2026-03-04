<template>
  <div class="flex h-screen overflow-hidden bg-cyber-900 text-gray-100 font-mono">
    <AppSidebar />
    <div class="flex flex-col flex-1 overflow-hidden">
      <AppNavbar />
      <main class="flex-1 overflow-y-auto p-4">
        <RouterView v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </RouterView>
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from "@/components/layout/AppSidebar.vue";
import AppNavbar  from "@/components/layout/AppNavbar.vue";
import AppFooter  from "@/components/layout/AppFooter.vue";
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
