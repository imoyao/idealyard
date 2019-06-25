import axios from 'axios'
import base from '@/api'

export const reqHotTags = params => {
  return axios.get(`${base}/posts`, {params: params}).then(res => res.data)
}
