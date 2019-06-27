#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/27 22:34
from flask import make_response, jsonify


def jsonify_with_status_code(data, code=200):
    """
    返回json数据同时修改返回状态码
    :param data:
    :param code:
    :return:
    """
    assert isinstance(data, dict)
    return make_response(jsonify(data), code)
