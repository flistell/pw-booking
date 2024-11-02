// import './assets/main.css'

import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap";

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
library.add(fas)
library.add(far)
library.add(fab)

import { createApp } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import router from './router';
const pinia = createPinia()
const app = createApp(App);
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(pinia)
app.use(router);
app.mount('#app');
