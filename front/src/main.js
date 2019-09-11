import Vue from 'vue'
import App from './App'

import router from './router'
import store from './store'

import lodash from 'lodash'

import ElementUI, {Message} from 'element-ui'
import '@/assets/theme/index.css'
import '@/assets/iyicon/iconfont.css'

import {formatTime} from "./utils/time";


Vue.config.productionTip = false


// 为了实现Class的私有属性
const showMessage = Symbol('showMessage')


// 重写ElementUI的Message
// 如何让Element UI的Message消息提示每次只弹出一个:https://segmentfault.com/a/1190000020173021
// single默认值true，因为项目需求，默认只弹出一个，可以根据实际需要设置

class DonMessage {
  success(options, single = true) {
    this[showMessage]('success', options, single)
  }

  warning(options, single = true) {
    this[showMessage]('warning', options, single)
  }

  info(options, single = true) {
    this[showMessage]('info', options, single)
  }

  error(options, single = true) {
    this[showMessage]('error', options, single)
  }

  [showMessage](type, options, single) {
    if (single) {
      // 判断是否已存在Message
      if (document.getElementsByClassName('el-message').length === 0) {
        Message[type](options)
      }
    } else {
      Message[type](options)
    }
  }
}

Vue.use(ElementUI)
Vue.prototype.$message = new DonMessage()
Object.defineProperty(Vue.prototype, '$_', {value: lodash})


Vue.directive('title', function (el, binding) {
  document.title = el.dataset.title
})
// 格式化时间
Vue.filter('format', formatTime)

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {App}
})
