import { createApp } from "vue";
import {createBootstrap} from 'bootstrap-vue-next';
import axios from 'axios';

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";


import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.BASE_URL ? process.env.BASE_URL : 'http://:8000/';

app.use(createBootstrap({components: true, directives: true}));
app.use(router);
app.use(store);
app.mount("#app");