#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/18 10:00
from flask import current_app, g
from sqlalchemy import or_
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from back.models import User, db

# 基础认证
basic_auth = HTTPBasicAuth()
# token认证
token_auth = HTTPTokenAuth()
# 混合认证（一个满足即可）
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(account, password):
    """
    基础认证回调函数，验证用户名和密码，if -> True，else False
    :param account:账号（用户名|邮箱）
    :param password:密码
    :return:
    """
    if not all((account, password)):
        return False
    else:
        user = User.query.filter(or_(User.username == account, User.email == account)).first()
        if not user or not user.verify_user_password(password):
            return False
        # user对像会被存储到Flask的g对象中
        g.user = user
        return True


def generate_auth_token(user_id, expiration=600):  # TODO:与models-User重复
    """
    生成含有user_id的token，有效时间10min  >> 10*60
    :param user_id:
    :param expiration:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    token = s.dumps({'id': user_id}).decode('ascii')
    return token


@token_auth.verify_token
def verify_token(token):
    """
    token认证
    :param token:
    :return:
    """
    g.user = None
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user_id = data.get('id')
    if data and user_id:
        user = User.query.get(user_id)
        g.user = user
        return True
    return False


class PostUserCtrl:

    @staticmethod
    def email_exists(email):
        return User.query.filter_by(email=email).one_or_none()

    @staticmethod
    def username_exists(username):
        return User.query.filter_by(username=username).one_or_none()

    @staticmethod
    def new_user(username, password, email):
        """
        创建新用户
        :param username: str,用户名
        :param password: str,密码
        :param email: str,邮箱
        :return:
        """
        user = User(email=email, username=username)
        hash_pw = user.hash_password(password)
        user.password = hash_pw
        db.session.add(user)
        db.session.commit()
        return user
