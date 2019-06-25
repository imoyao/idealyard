import axios from 'axios'
import base from '@/api'

// TODO: 根据请求参数返回

export const reqArticles = params => {
  return axios.get(`${base}/posts`, { params: params }).then(res => res.data)
}

export const reqHotArtices = params => {
  return axios.get(`${base}/posts`, { params: params }).then(res => res.data)
}

export const reqNewArtices = params => {
  return axios.get(`${base}/posts`, { params: params }).then(res => res.data)
}

export const reqHotTags = params => {
  return axios.get(`${base}/posts`, { params: params }).then(res => res.data)
}

export const reqArchives = params => {
  return axios.get(`${base}/posts`, { params: params }).then(res => res.data)
}

