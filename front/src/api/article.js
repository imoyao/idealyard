import request from '@/request'

// TODO: 里面很多api都是可以精简的

export function reqArticles(query, page) {
  return request({
    url: '/articles',
    method: 'get',
    params: {
      page: page.pageNumber,
      per_page: page.pageSize,
      name: page.name,
      sort: page.sort,
      year: query.year,
      month: query.month,
      tagId: query.tagId,
      categoryId: query.categoryId
    }
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
    url: `/articles/view/${id}`,
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
    url: '/articles/publish',
    method: 'post',
    data: article
  })
}

export function listArchives() {
  return request({
    url: '/articles/listArchives',
    method: 'get'
  })
}

export function reqArticleById(id) {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}
