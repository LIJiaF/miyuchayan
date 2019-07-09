import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Index = () => import('@/page/index.vue');
const Main = () => import('@/page/main.vue');
const UserList = () => import('@/page/user/list.vue');
const DiscountList = () => import('@/page/discount/list.vue');
const DiscountAdd = () => import('@/page/discount/add.vue');
const DiscountTypeList = () => import('@/page/discount_type/list.vue');
const DiscountTypeAdd = () => import('@/page/discount_type/add.vue');
const UserDiscountRel = () => import('@/page/user_discount_rel/list.vue');
const EditPassword = () => import('@/page/edit_password.vue');

Vue.use(Router);

const router = new Router({
  mode: 'hash',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Index',
      meta: {
        requireAuth: true
      },
      component: Index,
      children: [
        {
          path: '/main',
          name: 'Main',
          meta: {
            requireAuth: true
          },
          component: Main
        },
        {
          path: '/edit/password',
          name: 'EditPassword',
          meta: {
            requireAuth: true
          },
          component: EditPassword
        },
        {
          path: '/user',
          name: 'UserList',
          meta: {
            requireAuth: true
          },
          component: UserList
        },
        {
          path: '/discount',
          name: 'DiscountList',
          meta: {
            requireAuth: true
          },
          component: DiscountList
        },
        {
          path: '/discount/add',
          name: 'DiscountAdd',
          meta: {
            requireAuth: true
          },
          component: DiscountAdd
        },
        {
          path: '/discount/type',
          name: 'DiscountTypeList',
          meta: {
            requireAuth: true
          },
          component: DiscountTypeList
        },
        {
          path: '/discount/type/add',
          name: 'DiscountTypeAdd',
          meta: {
            requireAuth: true
          },
          component: DiscountTypeAdd
        },
        {
          path: '/user/discount/rel',
          name: 'UserDiscountRel',
          meta: {
            requireAuth: true
          },
          component: UserDiscountRel
        }
      ]
    },
    {
      path: '*',
      redirect: '/login'
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    let username = sessionStorage.getItem('username');
    if (username) {
      next();
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  }
  else {
    next();
  }
});

export default router;
