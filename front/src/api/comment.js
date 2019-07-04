import request from '@/request'


export function reqCommentsByArticle(id) {
  let paramsObj ={
    'post_id':id
  }
  return request({
    url: `/comments`,
    method: 'get',
    params:paramsObj
  })
}

export function publishComment(comment) {
  return request({
    url: '/comments/create/change',
    method: 'post',
    data: comment
  })
}

