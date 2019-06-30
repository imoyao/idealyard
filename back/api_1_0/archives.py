#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 22:16
"""
定义所有跟归档相关的api接口
"""
import json

from flask import g, jsonify, request
from flask import url_for, current_app
from flask_restful import Resource

from back import setting
from .errors import forbidden
from back.controller.tags import sort_tags, tag_detail, query_tag_item, makeup_tag_item_for_index
from back.models import Tag
from back.controller import archives
from .utils import jsonify_with_args
from back.models import db, Article, Category


class Archives(Resource):
    """
    文章归档
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        # 请求数据
        data = archives.extract_post_with_year_and_month()
        self.response_obj['data'] = data
        return jsonify(self.response_obj)


class ArchivesDetail(Resource):
    pass
