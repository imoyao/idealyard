#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

from . import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        """
        密码加密
        :param password:原始密码
        :return:
        """
        self.password = custom_app_context.encrypt(password)
        return self.password

    def verify_password(self, password):
        """
        验证密码
        :param password:str,原始密码
        :return:bool
        """
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=6000):
        """
        获取token，有效时间10min
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        使用token方式认证，解析token，确认登录的用户身份
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = User.query.get(data['id'])
        return admin
