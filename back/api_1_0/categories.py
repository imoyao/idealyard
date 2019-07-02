#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/1 11:05
"""

"""

from flask import request
from flask_restful import Resource

from back.controller import categories
from .utils import jsonify_with_args


class CategoryApi(Resource):
    """
    避免重名，起名*Api
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, category_id=None):
        # 请求数据
        args = request.args
        if category_id:
            data = categories.posts_for_category(category_id)
            self.response_obj['data'] = data
            return jsonify_with_args(self.response_obj)

        if args:
            # **注意**:args这里获取参数最好用dict.get() 而不是dict['key'],否则可能导致出错而程序不报错！！！
            pass
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)
        else:
            self.response_obj['data'] = categories.show_categories()
            return jsonify_with_args(self.response_obj)
