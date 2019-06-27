import request from '@/request'
import base from '@/api'
import axios from 'axios'

export const requestLogin = params => {
  return axios({method: 'POST', url: `${base}/login`, auth: params}).then(res => res.data)
}

// TODO:how to?
// export function requestLogin(account, password) {
//   const data = {
//     account,
//     password
//   }
//   return request({
//     url: '/login',
//     method: 'post',
//     auth: data
//     // data
//   })
// }

export function logout() {
  var _this = this
  this.$confirm('确认退出吗?', '提示', {
    type: 'warning'
  }).then(() => {
    sessionStorage.removeItem('token')
    _this.$router.push('/api/users')
  }).catch(() => {

  })
}

export function getUserInfo() {
  return request({
    url: '/users/currentUser',
    method: 'get'
  })
}

export function register(account, nickname, password) {
  const data = {
    account,
    nickname,
    password
  }
  return request({
    url: '/register',
    method: 'post',
    data
  })
}
