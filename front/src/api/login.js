import request from '@/request'
import base from '@/api'
import axios from 'axios'

export const requestLogin = params => {
  return axios({method: 'POST', url: `${base}/signin`, auth: params}).then(res => res.data)
}

// TODO:how to?
// export function requestLogin(account, password) {
//   const data = {
//     account,
//     password
//   }
//   return request({
//     url: '/signin',
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
    localStorage.removeItem('token')
    _this.$router.push('/')
  }).catch(() => {

  })
}

export function reqUserInfo() {
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
