import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Index = () => import('@/page/index.vue');
const UserList = () => import('@/page/user/list.vue');

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Index',
      component: Index,
      children: [
        {
          path: '/user',
          name: 'UserList',
          component: UserList
        }
      ]
    }
  ]
})
