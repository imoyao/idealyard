import request from '@/request'

export function requestLogin(account, password) {
  const data = {
    account,
    password
  }
  return request({
    method: 'POST',
    url: '/login',
    auth: data
    // data
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'get'
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
