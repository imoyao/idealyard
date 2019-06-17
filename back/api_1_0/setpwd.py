#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource

from back import setting
from back.models.db_user import User

auth = HTTPBasicAuth()


class Setpwd(Resource):
    def post(self):
        data = json.loads(str(request.data, encoding="utf-8"))
        admin = User.query.filter_by(name=setting.LOGINUSER).first()
        print(admin)
        if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
            admin.hash_password(data['newpass'])
            return jsonify({'code': 200, 'msg': "密码修改成功"})
        else:
            return jsonify({'code': 500, 'msg': "请检查输入"})
