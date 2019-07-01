import request from '@/request'

//
export function reqAllCategories() {
  return request({
    url: '/categories',
    method: 'get',
  })
}

// 带文章
// TODO:应该是查找文章该分类下的文章
export function reqCategoryDetail(id) {
  return request({
    url: `/categories/${id}`,
    method: 'get',
  })
}
