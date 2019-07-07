import request from '@/request'

//
export function reqAllCategories() {
  return request({
    url: '/categories',
    method: 'get',
  })
}

export function reqCategoryDetail(id) {
  return request({
    url: `/categories/${id}`,
    method: 'get',
  })
}
