import request from '@/request'

export function reqArticles(query, page) {
  let queryId = '', queryType = '', queryYear = '', queryMonth = ''
  if (query.tagId) {
    queryType = 'tag'
    queryId = query.tagId
  } else if (query.categoryId) {
    queryType = 'category'
    queryId = query.categoryId
  } else if (query.year && query.month) {
    queryType = 'archive'
    queryYear = query.year
    queryMonth = query.month
  }
  let paramsObj = {
    page: page.pageNumber,
    per_page: page.pageSize,
    order_by: page.orderBy,
    sort: page.sort,
  }
  switch (queryType) {
    case 'tag':
      queryId = query.tagId
      paramsObj.query_by = queryType
      paramsObj.tags = queryId
      break
    case 'category':
      queryId = query.categoryId
      paramsObj.query_by = queryType
      paramsObj.categories = queryId
      break
    case 'archive':
      paramsObj.query_by = queryType
      paramsObj.year = queryYear
      paramsObj.month = queryMonth
  }
  return request({
    url: '/articles',
    method: 'get',
    params: paramsObj
  })
}

export function reqHotArtices() {
  return request({
    url: '/articles',
    method: 'get',
    params: {
      hot: true,
      limit: 5,
    }
  })
}

export function reqPostid(identifier) {
  return request({
    url: '/identifiers',
    method: 'get',
    params: {
      identifier: identifier
    }
  })
}

export function reqNewArtices() {
  return request({
    url: '/articles',
    method: 'get',
    params: {
      new: true,
      limit: 5,
    }
  })
}

export function viewArticle(id) {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}

// 注意：此处和上边api走的后台逻辑基本一致，只是为了url好看
export function identiferArticle(identifierId) {
  return request({
    url: `/identifiers/${identifierId}`,
    method: 'get'
  })
}

export function identiferCount(identifierId) {
  return request({
    url: `/identifiers/${identifierId}`,
    method: 'patch',
    params: {
      field: 'count'
    }
  })
}

export function reqArticlesByCategory(id) {
  return request({
    url: `/articles/category/${id}`,
    method: 'get'
  })
}

export function reqArticlesByTag(id) {
  return request({
    url: `/articles/tag/${id}`,
    method: 'get'
  })
}


export function publishArticle(article) {
  return request({
    url: '/articles',
    method: 'post',
    data: article
  })
}

export function updateArticle(article) {
  const id = article.id
  return request({
    url: `/articles/${id}`,
    method: 'put',
    data: article
  })
}

export function listArchives(order) {
  let orderKey = order ? order : 'desc'
  return request({
    url: '/archives',
    method: 'get',
    params: {
      order: orderKey
    }
  })
}

export function reqArticleById(id) {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}

export function patchCount(id) {
  return request({
    url: `/articles/${id}`,
    method: 'patch',
    params: {
      field: 'count'
    }
  })
}

export function reqArticleSlug(title) {
  return request({
    url: `/slugs`,
    method: 'get',
    params: {
      title: title
    }
  })
}

export function deleteArticle(id,authorId) {
  const params = {
    authorId:authorId
  }
  return request({
    url: `/articles/${id}`,
    method: 'delete',
    data: params
  })
}
