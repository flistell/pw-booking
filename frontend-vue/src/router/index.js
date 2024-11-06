import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Items from '../components/Items.vue'
import Item from '../components/Item.vue'
import HomeView from '../views/HomeView.vue'
import BookingWizard from '@/views/BookingWizard.vue'
import CheckoutView from '@/views/CheckoutView.vue'
import LoginView from '@/views/LoginView.vue'
import BookingAdmin from '@/views/BookingAdmin.vue'
import { myAuthStore } from '@/stores/authUserStore'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
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
        to: route.query.to
      })
    },
    {
      path: '/admin',
      name: 'BookingAdmin',
      component: BookingAdmin
    },
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
});

router.beforeEach(async (to) => {
  const publicPages = [ '/login' ]
  const authRequired = !publicPages.includes(to.path);
  const authUserStore = myAuthStore();

  if (authRequired && !authUserStore.user) {
    authUserStore.returnUrl = to.fullPath;
    return '/login';
  }
});

export default router
