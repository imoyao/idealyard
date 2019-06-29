import request from '@/request'

export function reqAllTags() {
  return request({
    url: '/tags',
    method: 'get',
  })
}

export function reqAllTagsDetail() {
  return request({
    url: '/tags/detail',
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

export function reqTag(id) {
  return request({
    url: `/tags/${id}`,
    method: 'get',
  })
}

export function reqTagDetail(id) {
  return request({
    url: `/tags/detail/${id}`,
    method: 'get',
  })
}
