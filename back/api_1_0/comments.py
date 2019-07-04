#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/4 11:04

"""
定义所有跟评论相关的api接口
"""

from flask import jsonify,request
from flask_restful import Resource



class Comments(Resource):
    """
    文章归档
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self,comment_id=None):
        # 请求数据
        if comment_id:
            pass
        else:
            args = request.args
            print([_ for _ in args])
            if args:
                post_id = args.get('post_id')
                if post_id:
                    data = None
                    self.response_obj['data'] = data
            else:
                self.response_obj['code'] = 1
                self.response_obj['success'] = False
                self.response_obj['msg'] = 'Args required.'
        return jsonify(self.response_obj)



class ArchivesDetail(Resource):
    pass

