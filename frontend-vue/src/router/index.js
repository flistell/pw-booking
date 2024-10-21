import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Items from '../components/Items.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/items',
      name: 'Items',
      component: Items
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
  ]
})

export default router
