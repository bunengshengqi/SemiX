import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/demo',
      name: 'demo',
      component: () => import('../views/DemoView.vue'),
    },
    {
      path: '/trial',
      name: 'trial',
      component: () => import('../views/TrialView.vue'),
    },
    {
      path: '/policies',
      name: 'policies',
      component: () => import('../views/PoliciesView.vue'),
    },
    {
      path: '/suppliers',
      name: 'suppliers',
      component: () => import('../views/SuppliersView.vue'),
    },
    {
      path: '/market',
      name: 'market',
      component: () => import('../views/MarketIntelligenceView.vue'),
    },
    {
      path: '/compliance',
      name: 'compliance',
      component: () => import('../views/ComplianceToolsView.vue'),
    },
    {
      path: '/marketplace',
      name: 'marketplace',
      component: () => import('../views/MarketplaceView.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/CommunityView.vue'),
    },
    {
      path: '/community/create',
      name: 'community-create',
      component: () => import('../views/CommunityCreateView.vue'),
    },
    {
      path: '/community/:id',
      name: 'community-post',
      component: () => import('../views/CommunityPostView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
