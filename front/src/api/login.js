import request from '@/request'
import base from '@/api'
import axios from 'axios'
import {getToken} from '@/request/token'

export function requestLogin(account, password) {
  const data = {
    account,
    password
  }
  return request({
    url: '/signin',
    method: 'post',
    data
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
