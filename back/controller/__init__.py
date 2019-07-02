#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:17
from back.models import Article, Category, Tag


def category_for_post(category_id):
    """
    文章归档信息
    :param category_id: str(number)
    :return: dict
    """
    data = Category.query.get(category_id)
    if data:
        return {'categoryname': data.category_name,
                'id': category_id,
                'description': data.description,
                }


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


def assert_new_tag_in_tags(tags_for_new_post):
    tags = Tag.query.all()
    tags = set([tag.tag_name for tag in tags])
    print('------------tags_for_new_post', tags, tags_for_new_post)
    try:
        assert tags_for_new_post.issubset(tags)
    except AssertionError:
        need_add_tags = tags_for_new_post - tags
        return need_add_tags
