import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import MyStorage from '../views/MyStorage.vue'
import Share from '../views/Share.vue'
import HelloWorld from '../components/HelloWorld.vue'
import GroupList from '../views/GroupList.vue'
import GroupStorage from '../views/GroupStorage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: MyStorage
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
  {
    path: '/my-storage',
    name: 'FileRoot',
    component: MyStorage
  },
  {
    name: 'File',
    path: '/my-storage/:id',
    component: MyStorage
  },
  {
    path: '/share',
    component: Share
  },
  {
    path: '/share/:share_id'
  },
  {
    path: '/group-storage',
    component: GroupList
  },
  {
    name: 'GroupStorage',
    path: '/group-storage/:group_id',
    component: GroupStorage
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
