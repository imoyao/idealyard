#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/25 14:34

from flask import jsonify, request, g
from flask_restful import Resource

from back.models import User
from .utils import jsonify_with_args
from back.controller.authctrl import token_auth, PostUserCtrl,generate_auth_token

user_ctrl = PostUserCtrl()


def abort_if_not_exist(user_id):
    """
    操作之前需要保证操作存在，否则返回 404
    :param user_id:
    :return:
    """
    desc = 'The user {} not exist.'.format(user_id)
    user = User.query.get_or_404(user_id, description=desc)
    return user


class UserApi(Resource):
    """
    创建或者获取用户信息
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    @token_auth.login_required
    def get(self, user_id=None):
        data = dict()
        if user_id:
            user = abort_if_not_exist(user_id)
        else:
            user = g.user
        if user:
            data['account'] = user.name
            data['nickname'] = user.username
            # TODO:just for test
            data['avatar'] = '/static/user/admin.png'
            data['id'] = user.id
            self.response_obj['data'] = data
            return jsonify(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)

    def post(self):
        """
        新建用户（注册）
        :return:
        """
        json_data = request.json
        username = json_data.get('account')
        password = json_data.get('password')
        re_password = json_data.get('rePassword')
        email = json_data.get('email')
        if not all([username, password, email]):
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'Missing arguments.'
            return jsonify_with_args(self.response_obj, 400)
        if password != re_password:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'Please confirm password has been set correctly.'
            return jsonify_with_args(self.response_obj, 409)
        if user_ctrl.email_exists(email):
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj[
                'msg'] = 'Email address already exists,Please reset password or contact us to remove this account.'
            return jsonify_with_args(self.response_obj, 409)
        if user_ctrl.username_exists(username):
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            self.response_obj['msg'] = 'User name already exists,Please rename it.'
            return jsonify_with_args(self.response_obj, 409)

        data = dict()
        user = user_ctrl.new_user(username, password, email)
        user_id = user.id
        username = user.username
        token = generate_auth_token(user_id, expiration=60 * 120)
        data['token'] = token
        data['username'] = username
        self.response_obj['data'] = data
        return jsonify_with_args(self.response_obj, 201)
