import request from '@/request'

// TODO: 里面很多api都是可以精简的

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
