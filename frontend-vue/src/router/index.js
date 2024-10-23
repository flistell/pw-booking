import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Items from '../components/Items.vue'
//import Item from '../components/Item.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/items',
      name: 'Items',
      component: Items
    },
    // {
    //   path: '/item/:id?',
    //   name: 'Item',
    //   component: Item
    // },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
  ]
})

export default router
