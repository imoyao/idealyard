import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/Home'

import {Message} from 'element-ui';
import store from '@/store'

import {getToken} from '@/request/token'

import {requestLogin, reqUserInfo, logout, register} from '@/api/login'

Vue.use(VueRouter)

const router = new VueRouter({
  // https://router.vuejs.org/zh/guide/essentials/history-mode.html#html5-history-%E6%A8%A1%E5%BC%8F
  // mode: 'history',
  routes: [
    {
      path: '/write/:id?',
      component: r => require.ensure([], () => r(require('@/views/blog/BlogWrite')), 'blogwrite'),
      meta: {
        requireLogin: true
      },
    },
    {
      path: '/signin',
      component: r => require.ensure([], () => r(require('@/views/Login')), 'signin')
    },
    {
      path: '/register',
      component: r => require.ensure([], () => r(require('@/views/Register')), 'register')
    },
    {
      path: '',
      // name: 'Home',
      component: Home,
      children: [
        {
          path: '/',
          component: r => require.ensure([], () => r(require('@/views/Index')), 'index')
        },
        {
          path: '/log',
          component: r => require.ensure([], () => r(require('@/views/Log')), 'log')
        },
        {
          path: '/about',
          component: r => require.ensure([], () => r(require('@/views/About')), 'about')
        },
        {
          path: '/archives/:year?/:month?',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogArchive')), 'archives')
        },
        {
          path: '/messageBoard',
          component: r => require.ensure([], () => r(require('@/views/MessageBoard')), 'messageboard')
        },
        {
          // hint: 关于route传值 https://www.cnblogs.com/beka/p/8583924.html
          path: '/view/:id',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogView')), 'blogview')
        },
        {
          //TODO: tag & categroy 公用，后期可能给拆分开？
          path: '/:type',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogAllCategoryTag')), 'blogallcategorytag')
        },
        {
          path: '/:type/:id',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogCategoryTag')), 'blogcategorytag')
        }
      ]
    }

  ],
  scrollBehavior(to, from, savedPosition) {
    return {x: 0, y: 0}
  }
})

// 注册全局钩子拦截导航
router.beforeEach((to, from, next) => {
  if (getToken()) {
    console.log('1111111111')
    if (to.path === '/signin') {
      next({path: '/'})
    } else if (store.state.account.length === 0) {
      console.log('444444')
      store.dispatch('getUserInfo').then(data => { //获取用户信息
        console.log(data.data)
        next()
      }).catch(() => {
        console.log(response.status)
        next({path: '/signin'})
      })
      } else {
        next()
      }
      next()
    } else {
    if (to.matched.some(r => r.meta.requireLogin)) {
      console.log('22222222')
      Message({
        type: 'warning',
        showClose: true,
        message: '登录后才可以进行该操作哦~'
      })
      next('/signin')
    }
    else {
      console.log('33333333333333')
      next();
    }
  }
})


export default router
