#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 22:28
from back.controller import posts
from back.models import Article, Category

"""
分类 按照类别分组
"""


def posts_for_category(category_id):
    data = dict()
    articles = post_by_category_id(category_id)
    categories_data = posts.category_for_post(category_id)
    data['id'] = category_id
    data['article_counts'] = len(articles)
    data['categoryname'] = categories_data['categoryname']
    data['description'] = categories_data['description']
    return data


def show_categories():
    """
    显示所有的分类信息
    :return:
    """
    categories_data = Category.query.order_by(Category.id).all()
    print('--1111--', categories_data)
    all_data = []
    for category in categories_data:
        category_item = {}
        # hint:查询之后拿结果直接A.b 而不是 A[b]
        category_id = category.id
        articles = post_by_category_id(category_id)
        category_item['id'] = category.id
        category_item['article_counts'] = len(articles)
        category_item['articles'] = articles
        category_item['description'] = category.description
        category_item['categoryname'] = category.category_name
        all_data.append(category_item)
    return all_data


def post_by_category_id(category_id):
    """
    根据分类id查询分类下文章
    :param category_id: int,
    :return: list,post id in it
    """
    posts_data = Article.query.filter_by(category_id=category_id).all()
    articles = []
    if posts_data:
        articles = [data.post_id for data in posts_data]
    return articles
