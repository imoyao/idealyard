#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/25 14:34

from flask import jsonify, request, abort
from flask_restful import Resource

from back.models import User
from back.models import db


def abort_if_not_exist(user_id):
    """
    操作之前需要保证操作存在，否则返回 404
    :param user_id:
    :return:
    """
    desc = 'The user {} not exist.'.format(user_id)
    user = User.query.get_or_404(user_id, description=desc)
    return user


class CGUser(Resource):
    """
    创建或者获取用户信息
    """

    def get(self, user_id):
        user = abort_if_not_exist(user_id)
        return jsonify(user)

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if not all([username, password]):
            abort(400)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400)  # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username})
