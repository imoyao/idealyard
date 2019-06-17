#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g
from flask_restful import Resource


from back.models.db_user import User
from back import setting
auth = HTTPBasicAuth()


class Auth(Resource):
    """
    参考：https://www.cnblogs.com/vovlie/p/4182814.html
    """
    @auth.login_required
    def post(self):
        token = g.admin.generate_auth_token()
        if token:
            setting.LOGINUSER = g.admin.name
            return jsonify({'code': 200, 'msg': "success", 'token': token.decode('ascii'), 'name': g.admin.name})
        else:
            return jsonify({'code': 500, 'msg': "请检查输入"})


@auth.verify_password
def verify_password(name_or_token, password):
    """
    回调函数，验证用户名和密码，if -> True，else False
    :param name_or_token:
    :param password:
    :return:
    """
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = User.verify_auth_token(name_or_token)
    if not admin:
        admin = User.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    # user对像会被存储到Flask的g对象中
    g.admin = admin
    return True

