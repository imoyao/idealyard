import axios from 'axios'
import {Message} from 'element-ui'
import store from '@/store'
import {getToken} from '@/request/token'

const service = axios.create({
  baseURL: process.env.BASE_API,
  timeout: 10000
})

service.interceptors.request.use(function (config) {
  // Do something before request is sent
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, function (error) {
  // Do something with request error
  return Promise.reject(error)
})

// 响应拦截器
// Add a response interceptor
service.interceptors.response.use(function (response) {
  // Do something with response data
  return response.data
}, function (error) {
  console.log(error,'error')
  // Do something with response error
  if (error.response) {
      console.log(error.response,'error.response')
    // 匹配不同的响应码
    switch  (error.response.status) {
      case 401:
        // 清除 Token 及 已认证 等状态
        store.dispatch('fedLogOut').then(data => { //获取用户信息
          console.log(data.data)
          next()
        }).catch(() => {
          console.log(error.response)
        })
        // 跳转到登录页,对于登录用户直接跳，没有必要message
        //   Message({
        //   type: 'warning',
        //   showClose: true,
        //   message: '认证失败或登录超时，请检查登录信息！'
        // })
        break
      case 403:
        console.log(error)
        Message({
          type: 'error',
          showClose: true,
          message: '你没有权限进行该项操作！'
        })
        break
      case 404:
        Message({
          type: 'warning',
          showClose: true,
          message: '404: Not Found'
        })
        //TODO 页面跳转
        window.location.href="/"
        break

      case 500:  // 根本拿不到 500 错误，因为 CORs 不会过来
        Message({
          type: 'warning',
          showClose: true,
          message: '500: Oops... INTERNAL SERVER ERROR'
        })
        break
    }
  } else if (error.request) {
    Message({
          type: 'warning',
          showClose: true,
          message: '不好意思，我挂了。😕'
        })

    // Vue.toasted.error('The request has not been sent to Flask API，because OPTIONS get error', { icon: 'fingerprint' })
  } else {
    console.log('Error: ', error.message)
  }
  return Promise.reject(error)
})

export default service
