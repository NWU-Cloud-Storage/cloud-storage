import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import File from '../views/File.vue'
import HelloWorld from '../components/HelloWorld.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/hello',
    name: 'hello',
    component: HelloWorld
  },
  // {
  //   path: '/file',
  //   name: 'file',
  //   component: File
  // },
  {
    name: 'file',
    path: '/file/*',
    component: File
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
