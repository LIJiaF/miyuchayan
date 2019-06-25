import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
