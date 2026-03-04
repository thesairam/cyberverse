import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  { path: "/",               name: "Dashboard",      component: () => import("@/views/DashboardView.vue") },
  { path: "/intelligence",   name: "Intelligence",   component: () => import("@/views/IntelligenceView.vue") },
  { path: "/threats",        name: "Threats",        component: () => import("@/views/ThreatIntelView.vue") },
  { path: "/map",            name: "WorldMap",       component: () => import("@/views/WorldMapView.vue") },
  { path: "/financial",      name: "Financial",      component: () => import("@/views/FinancialView.vue") },
  { path: "/streams",        name: "Streams",        component: () => import("@/views/LiveStreamsView.vue") },
  { path: "/certifications", name: "Certifications", component: () => import("@/views/CertificationsView.vue") },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});
