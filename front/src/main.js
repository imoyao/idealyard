// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import ElementUI from 'element-ui'
import '@/assets/theme/index.css'
import '@/assets/icon/iconfont.css'

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.directive('title',  function (el, binding) {
  document.title = el.dataset.title
})

// 初始化axios
// https://segmentfault.com/a/1190000008470355
axios.defaults.baseURL = 'http://192.168.116.21:5000/api'
axios.defaults.auth = {
    username: '',
    password: '',
}
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})


// axios拦截器，401状态时跳转登录页并清除token
axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response) {
        switch (error.response.status) {
            case 401:
                store.commit('del_token')
                router.push('/login')
        }
    }
    return Promise.reject(error.response.data)
})


// 路由跳转
router.beforeEach((to, from, next) => {
    if (to.meta.required) {
        // 检查localStorage
        if (localStorage.token) {
            store.commit('set_token', localStorage.token)
            // 添加axios头部Authorized
            axios.defaults.auth = {
                username: store.state.token,
                password: store.state.token,
            }
            // iview的页面加载条
            iView.LoadingBar.start();
            next()
        } else {
            next({
                path: '/login',
            })
        }
    } else {
        iView.LoadingBar.start();
        next()
    }
})

router.afterEach((to, from, next) => {
    iView.LoadingBar.finish();
})
