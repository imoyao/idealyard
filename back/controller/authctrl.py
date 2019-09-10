#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/18 10:00
import hashlib
from flask import current_app, g
from sqlalchemy import or_
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from back.models import User, db
from back.utils import md5_encrypt
from back.utils.mail import MailSender
from back.utils.captcha import CaptchaCreator
from back.utils.redis_util import redis_store
from back import setting

sender = MailSender()
captcha_obj = CaptchaCreator()

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


#
# class TemporaryPassword:
#     """
#     see also:https://www.cnblogs.com/flashBoxer/p/9686059.html
#     https://www.cnblogs.com/coder2012/p/4309999.html
#     https://blog.csdn.net/qq_34564957/article/details/81017889
#     """
#
#     def __setattr__(self, verify_email, hash_pw):
#         """
#         设置临时密码
#         :param verify_email:str,
#         :param hash_pw:str,
#         :return:bool
#         """
#         set_success = redis_store.set(verify_email, hash_pw, ex=setting.TEMPORARY_PW_EXPIRE_SECONDS)
#         return set_success
#
#     def __getattr__(self, verify_email):
#         """
#         设置临时密码
#         :param verify_email:str,
#         :param hash_pw:str,
#         :return:bool
#         """
#         return redis_store.get(verify_email)
#
#     def __delattr__(self, verify_email):
#         """
#         设置过期
#         :param verify_email:
#         :return:
#         """
#         return redis_store.expire(verify_email, -1)

# @property
# def password(self):
#     return redis_store.get(verify_email)
#     # print('获取(get)属性时执行===')
#
# @password.setter
# def password(self, value):
#     print('设置(set)属性时执行===')
#
# @password.deleter
# def password(self):
#     print('删除(del)属性时执行===')


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

    @staticmethod
    def new_password(email, password):
        """
        创建新用户
        :param password: str,密码
        :param email: str,邮箱
        :return:
        """
        user = User.query.filter_by(email=email).one_or_none()
        if user:
            new_pw = user.hash_password(password)
            user.password = new_pw
            db.session.add(user)
            db.session.commit()
        return user

    @staticmethod
    def gen_captcha():
        return captcha_obj.shuffle()

    @staticmethod
    def makeup_send_reset_pw_mail(req_ip, captcha):
        """

        :param req_ip:
        :param captcha:
        :return:
        """
        email_data = dict()
        _subject = '重设别院牧志帐号密码'
        _body = f'''
已收到你的密码重设要求，请输入验证码：{captcha}，该验证码 {setting.TEMPORARY_PW_EXPIRE_MINUTES} 分钟内有效。
本次请求者IP为：{req_ip} ，若非您本人操作，请及时修改登录密码，以保证账户安全。 

感谢对 别院牧志 的支持，再次希望你在 别院牧志 的体验有益和愉快。

-- 别院牧志

(这是一封自动产生的 email ，请勿回复。)
'''
        email_data['subject'] = _subject
        email_data['body'] = _body
        return email_data

    def send_reset_pw_mail(self, req_ip, captcha, receiver):
        """
        同步发送邮件
        :param req_ip:
        :param captcha:
        :param receiver:
        :return:
        """
        _email_data = self.makeup_send_reset_pw_mail(req_ip, captcha)
        sender.send_mail(_email_data['subject'], receiver, _email_data['body'])

    @staticmethod
    def set_temporary_pw(verify_email, hash_pw):
        """
        设置临时密码
        :param verify_email:str,
        :param hash_pw:str,
        :return:bool
        """
        set_success = redis_store.set(verify_email, hash_pw, ex=setting.TEMPORARY_PW_EXPIRE_SECONDS)
        return set_success

    # TODO: see TemporaryPassword
    @staticmethod
    def get_temporary_pw(verify_email):
        """
        获取临时密码
        :param verify_email:str,
        :return:bool
        """
        return redis_store.get(verify_email)

    @staticmethod
    def expire_temporary_pw(verify_email):
        """
        密码过期
        :param verify_email:
        :return:
        """
        return redis_store.expire(verify_email, -1)

    def verify_temporary_pw(self, verify_email, temporary_pw):
        """
        通过email查询临时密码并校验，同时一次校验之后，将临时密码直接设置过期
        :param verify_email:
        :param temporary_pw:
        :return:
        """
        hash_pw = self.hash_temporary_pw(temporary_pw)
        rdb_get = self.get_temporary_pw(verify_email)
        self.expire_temporary_pw(verify_email)
        if rdb_get:
            str_rdb_get = rdb_get.decode('utf-8')  # byte >>> str
            return str_rdb_get == hash_pw
        else:
            return None  # 密码过期

    @staticmethod
    def hash_temporary_pw(temporary_pw):
        """
        加密临时密码
        :param temporary_pw:
        :return:
        """
        temporary_pw = str(temporary_pw) if isinstance(temporary_pw, int) else temporary_pw
        assert isinstance(temporary_pw, str)
        hash_pw = md5_encrypt(temporary_pw)
        return hash_pw

    def reset_pw_action(self, req_ip, verify_email):
        """
        更新用户临时密码到 redis 数据库（可设置过期时间），发送认证码邮件
        :param req_ip:str, 本次操作ip
        :param verify_email:str, 用户验证邮箱
        :return:
        """
        captcha = self.gen_captcha()
        hash_pw = self.hash_temporary_pw(captcha)
        set_success = self.set_temporary_pw(verify_email, hash_pw)
        if set_success:
            return self.send_reset_pw_mail(req_ip, captcha, verify_email)
        else:
            return 1
