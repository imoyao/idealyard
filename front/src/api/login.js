import request from '@/request'
import {getToken} from '@/request/token'

export function requestLogin(account, password) {
  const data = {
    username: account,
    password: password
  }
  return request({
    url: '/signin',
    method: 'post',
    auth:data,
    // 这里是重点，因为对配置不熟悉搞了好久。`auth` 表示应该使用 HTTP 基础验证，并提供凭据
    // 将设置一个 `Authorization` 头，覆写掉现有的任意使用 `headers` 设置的自定义 `Authorization`头
    // auth: {
    //   username: 'janedoe',
    //   password: 's00pers3cret'
    // },
  })
}

export function logout() {
  let _this = this
  this.$confirm('确认退出吗?', '提示', {
    type: 'warning'
  }).then(() => {
    localStorage.removeItem('token')
    _this.$router.push('/')
  }).catch(() => {

  })
}

export function reqUserInfo() {
  const data = {
    token:getToken()
  }
  return request({
    url: '/users',
    method: 'get',
    data
  })
}

export function register(userInfo) {
  let account = userInfo.account
  let email = userInfo.email
  let password = userInfo.password
  let rePassword = userInfo.rePassword
  const data = {
    account,
    email,
    password,
    rePassword
  }
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export function fetchCheckEmail(email) {
  return request({
    url: '/emails',
    method: 'get',
    params: email
  })
}
