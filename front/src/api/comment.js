import request from '@/request'


export function reqCommentsByArticle(id) {
  return request({
    url: `/comments/article/${id}`,
    method: 'get'
  })
}

export function publishComment(comment) {
  return request({
    url: '/comments/create/change',
    method: 'post',
    data: comment
  })
}

