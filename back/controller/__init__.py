#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:17
from back.models import Article, ArticleBody, Category, Tag, User
from back.utils import DateTime

date_maker = DateTime()


def assert_new_tag_in_tags(tags_for_new_post):
    tags = Tag.query.all()
    tags = set([tag.tag_name for tag in tags])
    print('------------tags_for_new_post', tags, tags_for_new_post)
    try:
        assert tags_for_new_post.issubset(tags)
    except AssertionError:
        need_add_tags = tags_for_new_post - tags
        return need_add_tags


def category_for_post(category_id):
    """
    文章归档信息p
    :param category_id: str(number)
    :return: dict
    """
    data = Category.query.get(category_id)
    if data:
        return {'categoryname': data.category_name,
                'id': category_id,
                'description': data.description,
                }


def author_info_for_post(user_id):
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
    if body:
        return {'id': body_id,
                'content': body.content,
                'contentHtml': body.content_html,
                'summary': body.summary,
                }


def tags_for_post(post_id):
    """
    根据文章 id 查找对应的 tags 信息
    ref:https://github.com/mrjoes/flask-admin/blob/402b56ea844dc5b215f6293e7dc63f39a6723692/examples/sqla/app.py
    https://www.jianshu.com/p/cd5b1728832c
    通过文章获取标签信息，重点在`posts_tags_table`的创建
    :param post_id: int,
    :return: dict,
    """
    article_obj = Article.query.filter(Article.post_id == post_id).first()
    tags_data = article_obj.tags
    tags_info = []
    if tags_data:
        # 标签信息列表
        tags_info = [{'id': tag.id, 'tag_name': tag.tag_name} for tag in tags_data]
    tag_count = len(tags_info)

    data = {
        'id': post_id,
        'tags_info': tags_info,
        'tag_count': tag_count
    }
    return data


def post_by_category_id(category_id):
    """
    根据分类id查询分类下文章
    :param category_id: int,
    :return: list,post id in it
    """
    posts_data = query_post_by_category(category_id)
    articles = []
    if posts_data:
        articles = [data.post_id for data in posts_data]
    return articles


def query_post_by_category(category_id, order_by='create_date', desc=True):
    """
    与上一个函数相比：一个返回query data 一个返回id list,可以合并  # TODO: 重复了！！！
    :param category_id:
    :param order_by:
    :param desc:
    :return:
    """
    posts_data = None
    if order_by == 'create_date':
        if desc:
            posts_data = Article.query.filter_by(category_id=category_id).order_by(Article.create_date.desc()).all()
        else:
            posts_data = Article.query.filter_by(category_id=category_id).order_by(Article.create_date).all()
    elif order_by == 'view_counts':
        if desc:
            posts_data = Article.query.filter_by(category_id=category_id).order_by(Article.view_counts.desc()).all()
        else:
            posts_data = Article.query.filter_by(category_id=category_id).order_by(Article.view_counts).all()
    return posts_data


def query_category(category_id):
    """
    根据 id 过滤 >> 返回
    :param category_id:
    :return:
    """
    return Article.query.filter_by(category_id=category_id)


def query_tag(tag_id):
    """
    根据 id 过滤 >> 返回
    :param tag_id:
    :return:
    """
    posts_data = Tag.query.filter_by(id=tag_id).one().articles
    return posts_data


def post_info_json(posts):
    """
    返回id与title键值对
    :param posts:list,
    :return: list,
    """
    ret_data = []
    for post in posts:
        post_info = dict()
        post_info['id'] = post.post_id
        post_info['identifier'] = post.identifier
        post_info['title'] = post.title
        ret_data.append(post_info)
    return ret_data


def make_tag_limit(query_data, limit_count):
    """
    是否对数量限制
    :param query_data:
    :param limit_count:
    :return:
    """
    if limit_count >= 1:
        # AttributeError: 'list' object has no attribute 'limit'
        data = query_data[:limit_count]
    else:
        data = query_data
    return data


def make_post_obj_limit(query_data, limit_count):
    post_data = make_tag_limit(query_data, limit_count)
    print(',0,11111111111111', post_data)
    data = makeup_post_item_for_index(post_data)
    return data


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
    shown_category_info = dict()

    for post_item in posts:
        user_id = post_item.author_id
        str_date = ''
        create_date = post_item.create_date
        if create_date:
            str_date = date_maker.make_strftime(create_date)

        #
        category_id = post_item.category_id
        post_id = post_item.post_id
        user_info = get_or_query(user_id, 'user')
        category_info = get_or_query(category_id, 'category')
        tag_infos = get_or_query(post_id, 'tag')['tags_info']
        username = user_info['nickname']
        post_content = content_for_post(post_id)
        summary = post_content.get('summary') or ''
        tags = []
        if tag_infos:
            tags = [{'tagname': tag.get('tag_name') or ''} for tag in tag_infos]
        post_info = {
            "author": {
                "nickname": username
            },
            # TODO: 继续开发
            "commentCounts": 0,
            "createDate": str_date,
            "id": post_item.post_id,
            "summary": summary,
            "tags": tags,
            "category": category_info,
            "title": post_item.title,
            "viewCounts": post_item.view_counts,
            "weight": post_item.weight
        }
        post_list.append(post_info)
    return post_list


def get_or_query(query_id, query_type):
    """
    一般来说：post数量大于user数量，所以我们这里在获取用户信息时先判断一下是否已经获取到了，没有获取到的话再去数据库中查询
    加载首页信息时，有的信息查询一次就可以了，没有必要每次循环都去数据库拿
    :return: query_id
    """
    unnecessary_every_time_dict = {
        'user': author_info_for_post(query_id),
        'category': category_for_post(query_id),
        'tag': tags_for_post(query_id)
    }
    shown_info = dict()
    str_query_id = str(query_id) if isinstance(query_id, int) else query_id
    assert isinstance(str_query_id, str)
    already_got = shown_info.get(str_query_id)
    if already_got:
        query_info = shown_info[str_query_id]
    else:
        query_info = unnecessary_every_time_dict.get(query_type)
        shown_info[str_query_id] = query_info
    return query_info
