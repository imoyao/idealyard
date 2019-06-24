#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import re
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource

from back import setting
from back.main.errors import unauthorized, forbidden
from back.models import User
from . import api

auth = HTTPBasicAuth()


class Auth(Resource):
    """
    参考：https://www.cnblogs.com/vovlie/p/4182814.html
    """

    @auth.login_required
    def post(self):
        token = g.user.generate_auth_token()
        print('------------', token)
        if token:
            setting.LOGINUSER = g.user.name
            return jsonify({'code': 200, 'msg': "success", 'token': token.decode('ascii'), 'name': g.user.name})
        else:
            return jsonify({'code': 500, 'msg': "请检查输入"})


class Setpwd(Resource):
    def post(self):
        data = json.loads(str(request.data, encoding="utf-8"))
        user = User.query.filter_by(name=setting.LOGINUSER).first()
        print(user)
        if user and user.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
            user.hash_password(data['newpass'])
            return jsonify({'code': 200, 'msg': "密码修改成功"})
        else:
            return jsonify({'code': 500, 'msg': "请检查输入"})


@auth.verify_password
def verify_password(name_or_token, password):
    """
    回调函数，验证用户名和密码，if -> True，else False
    :param name_or_token:用户名或者token
    :param password:密码
    :return:
    """
    print('------00--------', name_or_token)
    print('------11--------', password)
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    user = User.verify_auth_token(name_or_token)
    if not user:
        user = User.query.filter_by(username=name_or_token).first()
        if not user or not user.verify_password(password):
            return False
    # user对像会被存储到Flask的g对象中
    g.user = user
    return True


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    """
    想要在API访问前加login_required监护。
    为了让api蓝本中的所有API都一次性加上监护，可以用before_request修饰器应用到整个蓝本
    :return:
    """
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')
