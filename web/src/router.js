import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./views/HomeView.vue') },
    { path: '/chasers', component: () => import('./views/ChasersView.vue') },
    { path: '/escapees', component: () => import('./views/EscapeesView.vue') },
    { path: '/character/:faction/:id', component: () => import('./views/CharacterDetail.vue') },
    { path: '/maps', component: () => import('./views/MapsView.vue') },
    { path: '/maps/:id', component: () => import('./views/MapDetail.vue') },
    { path: '/versions', component: () => import('./views/VersionsView.vue') },
    { path: '/badges', component: () => import('./views/BadgesView.vue') },
    { path: '/stats', component: () => import('./views/StatsView.vue') }
  ],
  scrollBehavior() {
    return { top: 0 };
  }
});
