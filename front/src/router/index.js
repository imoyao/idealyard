import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/Home'
import HelloWorld from '@/components/HelloWorld'
import Index from '@/views/Index'
import Login from '@/views/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/',
          component: Index
        },
        // {
        //   path: '/log',
        //   component: r => require.ensure([], () => r(require('@/views/Log')), 'log')
        // },
        // {
        //   path: '/archives/:year?/:month?',
        //   component: r => require.ensure([], () => r(require('@/views/blog/BlogArchive')), 'archives')
        // },
        // {
        //   path: '/messageBoard',
        //   component: r => require.ensure([], () => r(require('@/views/MessageBoard')), 'messageboard')
        // },
        // {
        //   path: '/view/:id',
        //   component: r => require.ensure([], () => r(require('@/views/blog/BlogView')), 'blogview')
        // },
        // {
        //   path: '/:type/all',
        //   component: r => require.ensure([], () => r(require('@/views/blog/BlogAllCategoryTag')), 'blogallcategorytag')
        // },
        // {
        //   path: '/:type/:id',
        //   component: r => require.ensure([], () => r(require('@/views/blog/BlogCategoryTag')), 'blogcategorytag')
        // }
      ]

    },
    // {
    //   path: '/',
    //   name: 'Index',
    //   component: Index,
    //   meta: {
    //     required: true,
    //   }
    // },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    }
  ]
})
