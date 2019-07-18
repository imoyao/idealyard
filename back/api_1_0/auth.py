#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
参考
https://www.bbsmax.com/A/gVdnlP2QJW/
http://www.pythondoc.com/flask-restful/third.html
https://www.ctolib.com/docs/sfile/head-first-flask/chapter03/section3.05.html
"""

from flask import g, jsonify, request

from flask_restful import Resource

from back.models import User
from . import api_bp
from .errors import unauthorized, forbidden
from .utils import jsonify_with_args
from back.controller.authctrl import basic_auth, multi_auth, generate_auth_token


@basic_auth.error_handler
def unauthorized():
    return unauthorized('Unauthorized access')


@api_bp.before_request
@multi_auth.login_required
def before_request():
    """
    想要在API访问前加login_required监护。
    为了让api蓝本中的所有API都一次性加上监护，可以用before_request修饰器应用到整个蓝本
    :return:
    """
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


class Auth(Resource):
    """
    参考：https://www.cnblogs.com/vovlie/p/4182814.html
    https://www.cnblogs.com/PyKK2019/p/10889094.html
    """
    decorators = [basic_auth.login_required]

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def post(self):
        user_id = g.user.id
        token = generate_auth_token(user_id, expiration=60 * 120)
        if token:
            data = dict()
            username = g.user.username
            data['token'] = token
            data['username'] = username
            self.response_obj['data'] = data
            self.response_obj['msg'] = 'AUTHORIZED SUCCESS.'
            return jsonify_with_args(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'UNAUTHORIZED'
            return jsonify_with_args(self.response_obj, 401)

    def get(self):
        """
        /api/token 接口
        :return:
        """
        args = request.json
        username = args.get('username')
        # TODO: 用户id需要传值
        token = generate_auth_token(username)
        return jsonify({'token': token.decode('utf-8')})


class ResetPassword(Resource):
    """
    重置密码
    """

    # TODO:需要测试可用性
    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def post(self):
        """
        忘记密码：生成token,给用户发邮件，用户验证token通过，可以重置密码
        :return:
        """
        data = request.json
        verify_email = data.get('mail')
        user = User.query.filter_by(email=verify_email).one_or_none()
        if user:
            user_id = user.id
            token = generate_auth_token(user_id)  # TODO:需要组装发邮件
            return jsonify({'token': token.decode('utf-8')})

    @basic_auth.login_required
    def put(self):
        """
        更新密码（用户登录状态时重置密码）
        :return:
        """
        data = request.json
        verify_email = data.get('mail')
        # data = json.loads(str(request.data, encoding="utf-8"))
        user = User.query.filter_by(email=verify_email).one_or_none()
        if user and user.verify_user_password(data['oldpass']) and data['confirpass'] == data['newpass']:
            user.hash_password(data['newpass'])
            return jsonify({'code': 0, 'msg': "密码修改成功"})
        else:
            self.response_obj['code'] = 1
            self.response_obj['msg'] = 'Please check args.'
            return jsonify_with_args(jsonify(self.response_obj), 400)

    @multi_auth.login_required
    def get(self):
        """
        # 已注册用户访问该页面
        curl -u admin:123456 -i -X GET http://127.0.0.1:5000/api/password

        首先获取token:
        curl -u admin:123456 -i -X GET http://127.0.0.1:5000/api/token
        然后根据token访问页面：
        curl -u [token]:findpwd -i -X GET http://127.0.0.1:5000/api/password
        """
        username = g.user.username
        return jsonify({'msg': f'Hello, {username}! You have the right to reset password.',
                        'data': username})
