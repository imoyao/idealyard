#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:09
"""
定义所有跟标签相关的api接口
"""

from flask import jsonify, request
from flask_restful import Resource

from back import setting
from back.controller.tags import GetTagCtrl
from back.models import Tag
from .utils import jsonify_with_args

tag_getter = GetTagCtrl()


class TagApi(Resource):
    """
    避免重名，起名*Api  TODO: 这个函数里面获取的结构需要调整！！！
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, tag_id=None):
        # 请求数据
        query_by = 'tag_id'
        args = request.args
        if tag_id:
            # /api/tags/id
            query_key = tag_id
        elif args:
            # **注意**:args这里获取参数最好用dict.get() 而不是dict['key'],否则可能导致出错而程序不报错！！！
            query_key = args.get('name') and args['name'] or args.get('id') and args['id']
            hot = args.get('hot', False, type=bool)
            order = args.get('order')  # 默认降序
            order_by_desc = order and order == 'asc' or True
            limit_count = None
            if args.get('limit') and args['limit']:
                limit_count = int(args.get('limit'))
            if not limit_count:
                # 没有请求参数时，总数少于设定值则全返回，否则返回设定值
                limit_count = Tag.query.count() if Tag.query.count() < setting.LIMIT_HOT_TAG_COUNT else \
                    setting.LIMIT_HOT_TAG_COUNT
            # 最新最热走limit逻辑，截取而不是分页 TODO: 标签暂时应该没有这个必要
            page, per_page = (None,) * 2
            order_by = ''
            if not hot:
                # TODO:默认按照id排，后续可以添加按照名字排（index >> name）
                order_by = args.get('order_by', 'id', type=str)
        else:
            # 查全部
            self.response_obj['data'] = tag_getter.show_all_tags(limit_count=0)
            return jsonify_with_args(self.response_obj)
        # ?hot=true&limit=5
        data = tag_getter.get_tag_detail_by_args(query_key, query_by='tag_id', order_by=order_by, hot=hot,
                                                 order_by_desc=order_by_desc,
                                                 limit_count=limit_count)
        if data:
            self.response_obj['data'] = data
            return jsonify(self.response_obj)
        else:
            # 数据为空，还没来得及初始化！
            self.response_obj['code'] = 1
            self.response_obj['msg'] = 'Please for initialization.'
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 417)



class TagDetail(Resource):
    pass
