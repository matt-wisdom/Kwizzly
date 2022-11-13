import { createApp } from 'vue'
import App from './App.vue'
import '@/assets/css/tailwind.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './index.css'
import router from './router'

const app = createApp(App).use(router)
app.mount('#app')
app.use(VueAxios, axios)
