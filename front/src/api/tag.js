import request from '@/request'

export function reqAllTags() {
  return request({
    url: '/tags',
    method: 'get',
  })
}

export function reqHotTags() {
  return request({
    url: '/tags',
    method: 'get',
    params: {
      hot: true,
    }
  })
}

export function reqTagDetail(id) {
  return request({
    url: `/tags/${id}`,
    method: 'get',
  })
}
