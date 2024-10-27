import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Items from '../components/Items.vue'
import Item from '../components/Item.vue'
import HomeView from '../views/HomeView.vue'
import BookingWizard from '@/views/BookingWizard.vue'
import CheckoutView from '@/views/CheckoutView.vue'

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
    {
       path: '/items/:id?',
       name: 'Item',
       component: Item
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/checkout',
      name: 'CheckoutView',
      component: CheckoutView
    },
    {
      path: '/book' ,
      name: 'BookingWizard',
      component: BookingWizard,
      props: route => ({
        id: route.query.id,
        from: route.query.from,
        to: route.query.to,
        brand: route.query.brand,
        model: route.query.model,
        photo: route.query.photo
      })
    }
  ]
})

export default router
