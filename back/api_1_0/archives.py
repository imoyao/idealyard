#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 22:16
"""
定义所有跟归档相关的api接口
"""

from flask import jsonify, request
from flask_restful import Resource

from back.controller.archives import GetArchiveCtrl

Archives_getter = GetArchiveCtrl()


class Archives(Resource):
    """
    文章归档
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        # 请求数据
        order_desc = True
        args = request.args
        if args:
            order = args.get('order')
            # 默认降序，如果传值，则判断传值是否为desc,否? >> False
            order_desc = order and order == 'desc'
        data = Archives_getter.extract_post_with_year_and_month(order_desc)
        self.response_obj['data'] = data
        return jsonify(self.response_obj)


class ArchivesDetail(Resource):
    pass
