import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/Home'

import {Message} from 'element-ui';


import store from '@/store'

import {getToken} from '@/request/token'

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
          path: '/archives/:year?/:month?',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogArchive')), 'archives')
        },
        {
          path: '/messageBoard',
          component: r => require.ensure([], () => r(require('@/views/MessageBoard')), 'messageboard')
        },
        {
          path: '/view/:id',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogView')), 'blogview')
        },
        {
          path: '/:type',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogAllCategoryTag')), 'blogallcategorytag')
        },
        {
          path: '/:type/:id',
          component: r => require.ensure([], () => r(require('@/views/blog/BlogCategoryTag')), 'blogcategorytag')
        }
      ]
    },
    {
      path: '/signin',
      component: r => require.ensure([], () => r(require('@/views/Login')), 'signin')
    },
    {
      path: '/register',
      component: r => require.ensure([], () => r(require('@/views/Register')), 'register')
    }

  ],
  scrollBehavior(to, from, savedPosition) {
    return {x: 0, y: 0}
  }
})

// // 注册全局钩子拦截导航
// router.beforeEach((to, from, next) =>{
//   console.log('-----------------',getToken())
//   if (getToken()) {
//     if (to.path === '/signin') {
//       next({path: '/'})
//     } else {
//       next()
//       // if (store.state.account.length === 0) {
//       //   store.dispatch('getUserInfo').then(data => { //获取用户信息
//       //     next()
//       //   }).catch(() => {
//       //     next({path: '/'})
//       //   })
//       // } else {
//       //   next()
//       // }
//     }
//   }else {
//     if (to.matched.some(r => r.meta.requireLogin)) {
//       Message({
//         type: 'warning',
//         showClose: true,
//         message: '登录后才可以进行该操作哦~'
//       })
//       next('/signin')
//     }
//     else {
//       next();
//     }
//   }
// })

// router.beforeEach((to, from, next) => {
//
//   if (getToken()) {
//
//     if (to.path === '/signin') {
//       next({path: '/'})
//     } else {
//       if (store.state.account.length === 0) {
//         store.dispatch('getUserInfo').then(data => { //获取用户信息
//           next()
//         }).catch(() => {
//           next({path: '/'})
//         })
//       } else {
//         next()
//       }
//     }
//   } else {
//     if (to.matched.some(r => r.meta.requireLogin)) {
//       Message({
//         type: 'warning',
//         showClose: true,
//         message: '请先登录哦'
//       })
//
//     }
//     else {
//       next();
//     }
//   }
// })


export default router
