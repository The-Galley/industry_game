import { createRouter, createWebHistory } from 'vue-router';
import AboutView from '../views/AboutView.vue';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView';
import RegV from "@/views/RegV.vue";
import StartPage from "@/views/StartPage.vue";
import GameSelection from "@/views/GameSelection.vue";
import GameDesc from "@/views/GameDesc.vue";
import GameDescAdmin from "@/views/GameDescAdmin.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/gamereg',
    name: 'RegV',
    component: RegV,
  },
  {
    path: '/main',
    name: 'StartPage',
    component: StartPage,
  },
  {
    path: '/selectgame',
    name: 'SelectGame',
    component: GameSelection,
  },
  {
    path: '/gamedesc',
    name: 'GameDesc',
    component: GameDesc,
  },
  {
    path: '/gamedescadmin',
    name: 'GameDescAdmin',
    component: GameDescAdmin,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
