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
    """
    用户点击文章链接跳详情页的数据接口，返回在这里找
    :param post_info:
    :return:
    """
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
        # TODO:摘要，暂无；感觉这个api不需要该参数？？？
        # "summary": "本节将介绍如何在项目中使用 Element。",
        "tags": tag_infos,
        "title": post_info.title,
        "viewCounts": post_info.view_counts,
        "weight": post_info.top_it,
    }
    return json_post


def makeup_post_item_for_index(posts):
    """
    组装首页展示需要的数据
    :return:
    """
    '''
    [{
    "author":{
        "nickname":"imoyao"
    },
    "commentCounts":0,
    "createDate":"2019.02.28 15:37",
    "id":28,
    "summary":"sample summary",
    "tags":[
        {
            "tagname":"Python"
        }
    ],
    "title":"tt",
    "viewCounts":188,
    "weight":0
    },
    ……
    {……}
    ]
    '''
    post_list = []
    shown_user_info = dict()

    for post_item in posts:
        user_id = post_item.author_id
        str_user_id = str(user_id) if isinstance(user_id, int) else user_id
        already_got = shown_user_info.get(str_user_id)
        if already_got:
            user_info = shown_user_info[str_user_id]
        else:
            user_info = user_info_for_post(user_id)
            shown_user_info[str_user_id] = user_info
        username = user_info['nickname']
        post_id = post_item.post_id
        tag_infos = tags_for_post(post_id)
        tags = []
        if tag_infos:
            tags = [{'tagname': tag.get('tagname') or ''} for tag in tag_infos]
        post_info = {
            "author": {
                "nickname": username
            },
            # TODO: 继续开发
            "commentCounts": 0,
            "createDate": post_item.create_date,
            "id": post_item.post_id,
            # TODO: 继续开发
            "summary": "sample summary",
            "tags": tags,
            "title": post_item.title,
            "viewCounts": post_item.view_counts,
            "weight": post_item.top_it
        }
        post_list.append(post_info)
    return post_list


def user_info_for_post(user_id):
    """
    文章作者信息
    :param user_id: str(number),author_id
    :return: dict,
    """
    user = User.query.get(user_id)
    if user:
        return {'avatar': user.avatar_hash,
                'id': user_id,
                'nickname': user.username,
                }


def content_for_post(body_id):
    """
    获取文章正文内容
    TODO: 因为此处返回表所有的数据，所以是否可以直接返回，不需要手动组装（只是修改前端获取的字段键）
    :param body_id: str(number)
    :return: dict
    """
    body = ArticleBody.query.get(body_id)
    # https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    print('see what get--------------', body)
    if body:
        return {'content': body.content,
                'contentHtml': body.content_html,
                'id': body_id,
                }


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
