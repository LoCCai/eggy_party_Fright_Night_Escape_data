import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('./views/LoginView.vue') },
    {
      path: '/',
      component: () => import('./views/Layout.vue'),
      children: [
        { path: '', component: () => import('./views/DashboardView.vue') },
        { path: 'chasers', component: () => import('./views/CharacterManage.vue'), meta: { faction: 'chasers' } },
        { path: 'escapees', component: () => import('./views/CharacterManage.vue'), meta: { faction: 'escapees' } },
        { path: 'maps', component: () => import('./views/MapManage.vue') },
        { path: 'patches', component: () => import('./views/PatchManage.vue') },
        { path: 'badges', component: () => import('./views/BadgeManage.vue') }
      ]
    }
  ]
});

router.beforeEach((to) => {
  if (to.path !== '/login' && !localStorage.getItem('fne:token')) return '/login';
  if (to.path === '/login' && localStorage.getItem('fne:token')) return '/';
});
