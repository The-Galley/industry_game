import { createRouter, createWebHistory } from 'vue-router';
import AboutView from '../views/AboutView.vue';
import RegV from "@/views/RegV.vue";
import StartPage from "@/views/StartPage.vue";
import GameSelection from "@/views/GameSelection.vue";
import GameDesc from "@/views/GameDesc.vue";
import GameDescAdmin from "@/components/GameDescAdmin.vue";
import LogV from "@/views/LogV.vue";
import CreateGame from "@/views/CreateGame.vue";
import GameStartTimer from "@/views/GameStartTimer.vue";

import { useStore } from 'vuex';

const routes = [
  {
    path: '/about',
    name: 'About',
    component: AboutView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LogV,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegV,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'StartPage',
    component: StartPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/games',
    name: 'SelectGame',
    component: GameSelection,
    meta: { requiresAuth: true }
  },
  {
    path: `/games/:gameId`,
    name: 'GameDesc',
    component: GameDesc,
    meta: { requiresAuth: true }
  },
  {
    path: `/games/admin/:gameId`,
    name: 'GameDescAdmin',
    component: GameDescAdmin,
    meta: { requiresAuth: true }
  },
  {
    path: '/creategame',
    name: 'CreateGame',
    component: CreateGame,
    meta: { requiresAuth: true }
  },
  {
    path: '/timer',
    name: 'GameStartTimer',
    component: GameStartTimer,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const store = useStore();
  const isAuthenticated = store.getters.isAuthenticated;
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'StartPage' });
  } else if (!to.meta.requiresAuth && isAuthenticated) {
    next({ name: 'SelectGame' });
  } else {
    next();
  }
});

export default router;
