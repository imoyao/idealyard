#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/24 16:40
"""
定义所有跟文章相关的api接口
"""
import json

from flask import g, jsonify, request
from flask import url_for, current_app
from flask_restful import Resource

from back import setting
from back.controller import posts
from back.models import Article
from . import api
from .errors import forbidden
from .utils import jsonify_with_args


def abort_if_not_exist(post_id):
    """
    操作之前需要保证操作的文章存在，否则返回 404
    :param post_id:
    :return:
    """
    desc = 'The post {} not exist.'.format(post_id)
    post = Article.query.get_or_404(post_id, description=desc)
    return post


class PostApi(Resource):
    """
    获取文章列表（分页展示及条件查询）
    """
    '''
    1.5 避免多级 URL
    常见的情况是，资源需要多级分类，因此很容易写出多级的 URL，比如获取某个作者的某一类文章。

    GET /authors/12/categories/2
    这种 URL 不利于扩展，语义也不明确，往往要想一会，才能明白含义。

    更好的做法是，除了第一级，其他级别都用查询字符串表达。

    GET /authors/12?categories=2
    下面是另一个例子，查询已发布的文章。你可能会设计成下面的 URL。
    GET /articles/published
    查询字符串的写法明显更好。
    GET /articles?published=true

    如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。
    下面是一些常见的参数。

    ?limit=10：指定返回记录的数量
    ?offset=10：指定返回记录的开始位置。
    ?page=2&per_page=100：指定第几页，以及每页的记录数。
    ?order_by=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
    ?animal_type_id=1：指定筛选条件
    参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /zoo/ID/animals 与 GET /animals?zoo_id=ID 的含义是相同的。
    '''

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        # 请求数据
        args = request.args
        print([_ for _ in args])
        if args:
            # **注意**:args这里获取参数最好用dict.get() 而不是dict['key'],否则可能导致出错而程序不报错！！！
            # ?new=true
            new = args.get('new', False, type=bool)
            # ?hot=true
            hot = args.get('hot', False, type=bool)
            # ?order = asc
            order = args.get('order')  # 默认降序
            order_by_desc = order and order == 'asc' or True  # 暂时默认是降序
            # ?limit=5
            limit_count = int(args.get('limit')) if args.get('limit') else setting.LIMIT_NEW_POST_COUNT
            # 最新最热走limit逻辑，截取而不是分页
            page, per_page = (None,) * 2
            order_by = ''
            # 如果是最新或者最热，表示order_by已经传值，不能重新赋值！
            if not (new or hot):
                # ?page=1&per_page=10
                page = args.get('page', 1, type=int)
                # TODO:变量来自于setting还是config应该统一！！！
                per_page = args.get('per_page', type=int) or current_app.config['FLASKY_POSTS_PER_PAGE']
                # ?order_by=create_date
                order_by = args.get('order_by', 'create_date', type=str)
            print('order-by', order_by)
            # ?new=true&limit=5
            query_data = None
            if new or order_by == 'create_date':
                query_data = posts.posts_order_by_date(desc=order_by_desc)
            # ?hot=true&limit=5
            elif hot or order_by == 'view_counts':
                query_data = posts.posts_order_by_view_counts(desc=order_by_desc)
            # print(query_data_sql)
            if query_data:
                # ?page=1&per_page=10?order_by=name&order=asc
                if all([page, per_page]):
                    pagination = posts.make_paginate(query_data, page=page, per_page=per_page)
                    prev_page, next_page, data = self.parse_pagination(pagination, page=page, per_page=per_page)
                    self.response_obj['data'] = data
                    self.response_obj['prev'] = prev_page
                    self.response_obj['next'] = next_page
                    self.response_obj['total'] = pagination.total
                else:
                    data = posts.make_limit(query_data, limit_count)
                    self.response_obj['data'] = data
            return jsonify(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'No args.'
            return jsonify_with_args(self.response_obj, 400)

    @staticmethod
    def parse_pagination(pagination, page=None, per_page=None):
        _posts_list = pagination.items
        prev_page = None
        # https://stackoverflow.com/questions/24223628/how-do-i-use-flask-url-for-with-flask-restful
        if pagination.has_prev:
            prev_page = api.url_for(PostApi, page=page - 1, per_page=per_page, _external=True)
        next_page = None
        if pagination.has_next:
            next_page = api.url_for(PostApi, page=page + 1, per_page=per_page, _external=True)

        data = posts.makeup_post_item_for_index(_posts_list)
        return prev_page, next_page, data


class PostDetail(Resource):
    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, post_id):
        """
        获得指定ID对应的文章
        :param post_id: int,
        :return: json,
        """
        post = abort_if_not_exist(post_id)
        post_info = posts.post_detail(post)
        self.response_obj['data'] = post_info
        return jsonify(self.response_obj)

    def post(self, post_id):
        """
        创建指定id文章
        :return:
        """
        # 获取post请求参数
        # https://blog.csdn.net/longting_/article/details/80637002
        post = Article.query.get(post_id)
        if post:
            self.response_obj['error'] = 'Invalid post id.'
            self.response_obj['data'] = ''
            self.response_obj['msg'] = 'Create an exist post is impossible.'
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)
        else:
            json_data = request.get_json()
            post = Article.from_json(json_data)
            post.author_id = g.current_user  # TODO:用户登录之后保存用户名称和用户id
            Article.insert_new_post(post)  # TODO:need func()
            # 服务器为新资源指派URL，并在响应的Location首部中返回
            return jsonify_with_args(post.to_json()), 201, {
                'Location': url_for('api.articles', id=post.id, _external=True)}

    def put(self, post_id):
        """
        更新指定文章
        注意：必须是原作者，TODO:管理员可以折叠或隐藏？后期开发
        :param post_id:
        :return:
        """
        post = abort_if_not_exist(post_id)
        # if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        if g.current_user != post.author_id:  # TODO:此处必须保证唯一
            return forbidden('Insufficient permissions')
        recvdata = json.loads(str(request.data, encoding="utf-8"))
        if recvdata:
            poster = recvdata['params']
            Article.update_post_by_id(post_id, poster)
        return jsonify(post.to_json())

    def delete(self, post_id):
        """
        删除指定文章
        :param post_id: int
        :return:
        """
        post = abort_if_not_exist(post_id)
        # if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        if g.current_user != post.author_id:  # TODO:此处必须保证唯一，除了用户本人，管理员应该也可以删除
            return forbidden('Insufficient permissions')
        Article.delete_post(post)
        return jsonify(post.to_json())
