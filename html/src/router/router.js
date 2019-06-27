import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Index = () => import('@/page/index.vue');
const UserList = () => import('@/page/user/list.vue');
const DiscountList = () => import('@/page/discount/list.vue');
const DiscountTypeList = () => import('@/page/discount_type/list.vue');
const UserDiscountRel = () => import('@/page/user_discount_rel/list.vue');

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
        },
        {
          path: '/discount',
          name: 'DiscountList',
          component: DiscountList
        },
        {
          path: '/discount/type',
          name: 'DiscountTypeList',
          component: DiscountTypeList
        },
        {
          path: '/user/discount/rel',
          name: 'UserDiscountRel',
          component: UserDiscountRel
        }
      ]
    }
  ]
})
