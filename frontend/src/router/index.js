import { createRouter, createWebHistory } from 'vue-router';
import AboutView from '../views/AboutView.vue';
import RegV from "@/views/RegV.vue";
import StartPage from "@/views/StartPage.vue";
import GameSelection from "@/views/GameSelection.vue";
import GameDesc from "@/views/GameDesc.vue";
import GameDescAdmin from "@/views/GameDescAdmin.vue";
import LogV from "@/views/LogV.vue";
import CreateGame from "@/views/CreateGame.vue";
import GameStartTimer from "@/views/GameStartTimer.vue";

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
  },
  {
    path: '/register',
    name: 'Register',
    component: RegV,
  },
  {
    path: '/',
    name: 'StartPage',
    component: StartPage,
  },
  {
    path: '/games',
    name: 'SelectGame',
    component: GameSelection,
  },
  {
    path: `/games/:gameId`,
    name: 'GameDesc',
    component: GameDesc,
  },
  {
    path: `/games/admin/:gameId`,
    name: 'GameDescAdmin',
    component: GameDescAdmin,
  },
  {
    path: '/creategame',
    name: 'CreateGame',
    component: CreateGame,
  },
  {
    path: '/timer',
    name: 'GameStartTimer',
    component: GameStartTimer,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
