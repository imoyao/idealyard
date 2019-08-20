#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/25 14:34

from flask import jsonify, request, abort, g
from flask_restful import Resource

from back.models import User
from back.models import db
from .utils import jsonify_with_args
from back.controller.authctrl import token_auth


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
        username = json_data.get('username')
        password = json_data.get('password')
        if not all([username, password]):
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(409)  # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify_with_args({'username': user.username}, 201)
