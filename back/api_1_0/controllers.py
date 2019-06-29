#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 6:12
from flask import jsonify
from back.models import User, ArticleBody, Article, Category


def post_info_json(posts):
    """
    返回id与title键值对
    :param posts:list,
    :return: list,
    """
    print(type(posts))
    ret_data = []
    for post in posts:
        post_info = dict()
        post_info['id'] = post.post_id
        post_info['post_url_id'] = post.identifier
        post_info['title'] = post.title
        ret_data.append(post_info)
    return ret_data


def post_detail(post_info):
    user_id = post_info.author_id
    user_info = user_info_for_post(user_id)
    body_id = post_info.body_id
    body_info = content_for_post(body_id)

    category_id = post_info.category_id
    category_info = category_for_post(category_id)
    post_id = post_info.post_id
    tag_infos = tags_for_post(post_id)
    json_post = {
        "author": user_info,
        "body": body_info,
        "category": category_info,
        # TODO:后期添加
        "commentCounts": 0,
        "createDate": post_info.create_date,
        "id": post_id,
        # TODO:摘要，暂无；感觉这个api不需要这个参数？？？
        # "summary": "本节将介绍如何在项目中使用 Element。",
        "tags": tag_infos,
        "title": post_info.title,
        "viewCounts": post_info.view_counts,
        "weight": post_info.top_it,
    }
    return json_post


def user_info_for_post(user_id):
    user = User.query.get(user_id)

    if user:
        return {'avatar': user.avatar_hash,
                'id': user_id,
                'nickname': user.username,
                }


def content_for_post(body_id):
    # TODO: 因为此处返回表所有的数据，所以是否可以直接返回，不需要手动组装（只是修改前端获取的字段键）
    body = ArticleBody.query.get(body_id)
    # https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    print('see what get--------------', body)
    if body:
        return {'content': body.content,
                'contentHtml': body.content_html,
                'id': body_id,
                }


def category_for_post(category_id):
    data = Category.query.get(category_id)
    if data:
        return {'categoryname': data.category_name,
                'id': category_id,
                }


def tags_for_post(post_id):
    """
    ref:https://github.com/mrjoes/flask-admin/blob/402b56ea844dc5b215f6293e7dc63f39a6723692/examples/sqla/app.py
    https://www.jianshu.com/p/cd5b1728832c
    通过文章获取标签信息，重点在`posts_tags_table`的创建
    :param post_id: int,
    :return: list,
    """
    article_obj = Article.query.filter(Article.post_id == post_id).first()
    tags = article_obj.tags
    tag_infos = []
    for tag_item in tags:
        tag = dict()
        tag['id'] = tag_item.id
        tag['tagname'] = tag_item.tag_name
        tag_infos.append(tag)
    return tag_infos
