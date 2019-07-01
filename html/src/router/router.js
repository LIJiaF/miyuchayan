import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Index = () => import('@/page/index.vue');
const UserList = () => import('@/page/user/list.vue');
const DiscountList = () => import('@/page/discount/list.vue');
const DiscountAdd = () => import('@/page/discount/add.vue');
const DiscountTypeList = () => import('@/page/discount_type/list.vue');
const DiscountTypeAdd = () => import('@/page/discount_type/add.vue');
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
          path: '/discount/add',
          name: 'DiscountAdd',
          component: DiscountAdd
        },
        {
          path: '/discount/type',
          name: 'DiscountTypeList',
          component: DiscountTypeList
        },
        {
          path: '/discount/type/add',
          name: 'DiscountTypeAdd',
          component: DiscountTypeAdd
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
