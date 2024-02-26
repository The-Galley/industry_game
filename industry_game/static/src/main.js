import "bootstrap/dist/css/bootstrap.css";
import { createApp } from "vue";
import axios from 'axios';

import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000/';

app.use(router);
app.use(store);
app.mount("#app");