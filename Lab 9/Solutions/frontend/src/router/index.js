import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Logout.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/messages/:id',
    name: 'Messages',
    component: () => import('../views/Messages.vue')
  },
  {
    path: '/online',
    name: 'Online',
    component: () => import('../views/Online.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
