#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:09
"""
定义所有跟标签相关的api接口
"""
import json

from flask import g, jsonify, request
from flask import url_for, current_app
from flask_restful import Resource

from back import setting
from .errors import forbidden
from back.controller.tags import sort_tags, tag_detail, query_tag_item, makeup_tag_item_for_index
from back.models import Tag
from back.controller import posts
from .utils import jsonify_with_args
from back.models import db, Article, posts_tags_table


class TagApi(Resource):
    """
    避免重名，起名*Api
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0}

    def get(self):
        # 请求数据
        args = request.args

        if args:
            # **注意**:args这里获取参数最好用dict.get() 而不是dict['key'],否则可能导致出错而程序不报错！！！
            hot = args.get('hot', False, type=bool)
            order = args.get('order', True, type=bool)  # 默认降序
            print(order)
            limit_count = None
            # ?hot=true&limit=5
            if hot:
                if args.get('limit') and args['limit']:
                    limit_count = int(args.get('limit'))
                if not limit_count:
                    # 没有请求参数时，总数少于设定值则全返回，否则返回设定值
                    limit_count = Tag.query.count() if Tag.query.count() < setting.LIMIT_HOT_TAG_COUNT else setting.LIMIT_HOT_TAG_COUNT
                # TODO:此处实现十分不优雅，感觉绕了好大一个圈，需要优化优化优化！！！
                info = query_tag_item(limit_count)
                tags_sorted = sort_tags(info, reverse=order)
                self.response_obj['data'] = makeup_tag_item_for_index(tags_sorted)
                return jsonify(self.response_obj)
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)


class TagDetail(Resource):
    pass
