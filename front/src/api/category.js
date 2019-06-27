import request from '@/request'

export function reqAllCategorys() {
  return request({
    url: '/categorys',
    method: 'get',
  })
}

export function reqAllCategorysDetail() {
  return request({
    url: '/categorys/detail',
    method: 'get',
  })
}

export function reqCategory(id) {
  return request({
    url: `/categorys/${id}`,
    method: 'get',
  })
}

export function reqCategoryDetail(id) {
  return request({
    url: `/categorys/detail/${id}`,
    method: 'get',
  })
}
