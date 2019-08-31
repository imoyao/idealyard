#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/27 22:34
from flask import make_response, jsonify


def jsonify_with_args(data, code=200, *args):
    """
    返回json数据同时修改返回状态码,etc
    :param data:
    :param code:
    :param args:
    :return:
    """
    assert isinstance(data, dict)
    return make_response(jsonify(data), code, *args)
