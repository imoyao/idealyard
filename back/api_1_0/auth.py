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
from . import api
from back.api_1_0.errors import unauthorized_error, forbidden
from .utils import jsonify_with_args
from back.controller.authctrl import basic_auth, multi_auth, PostUserCtrl, generate_auth_token
from back.celery_components import tasks as celery_tasks
from back.api_1_0 import api_tasks

auth_ctrl = PostUserCtrl()


@basic_auth.error_handler
def unauthorized(*args, **kwargs):
    return unauthorized_error('Unauthorized access')


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

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def post(self):
        """
        忘记密码：生成token,给用户发邮件，用户验证token通过，可以重置密码
        :return:
        """
        data = request.json
        verify_email = data.get('email')
        reset_password = data.get('password')
        user = auth_ctrl.new_password(verify_email, reset_password)
        data['username'] = user.username
        data['email'] = user.email
        self.response_obj['data'] = data
        self.response_obj['msg'] = ''
        return jsonify_with_args(self.response_obj)

    @basic_auth.login_required
    def put(self):
        """
        更新密码（用户登录状态时重置密码）
        :return:
        """
        data = request.json
        verify_email = data.get('mail')
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


class EmailApi(Resource):
    """
    验证邮箱
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        args = request.args
        if args:
            email = args.get('email', '')
            if auth_ctrl.email_exists(email):
                return jsonify_with_args(self.response_obj, 200)
            self.response_obj = {'status': '404', 'success': False, 'code': 0, 'data': None,
                                 'msg': 'The email address has not register for this site.'}
            return jsonify_with_args(self.response_obj, 200)
        else:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)

    def post(self):
        json_data = request.json
        try:
            req_ip = request.headers['X-Forwarded-For'].split(',')[0]  # 反向代理之后
        except KeyError:
            req_ip = request.remote_addr
        email = json_data.get('email')
        if email:
            # 此处使用celery发送重置邮件
            # TODO: 此处应该有失败和成功状态记录
            task = celery_tasks.send_reset_password_mail_long_task.apply_async(args=(req_ip, email), queue='mail',
                                                                               routing_key='mail')
            self.response_obj['msg'] = 'Send mail success,please check your mail box.'
            resp = jsonify_with_args(self.response_obj, 201, {
                'Location': api.url_for(api_tasks.TaskStatus, task_id=task.id, name='mail', _external=True)})
            # 跨域设置
            # see also: https://segmentfault.com/a/1190000009125333
            # https://www.jianshu.com/p/e2cdc73f85bc
            resp.headers['Access-Control-Expose-Headers'] = 'location'
            return resp
            # ret_code = auth_ctrl.reset_pw_action(req_ip, email)
            # if not ret_code:
            #     self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}
            #     return jsonify_with_args(self.response_obj, 200)
            # else:
            #     self.response_obj = {'success': False, 'code': 1, 'data': None, 'msg': 'Send reset password mail fail.'}
            #     return jsonify_with_args(self.response_obj, 408)
        else:
            self.response_obj = {'success': False, 'code': 1, 'data': None,
                                 'msg': 'Need email address for sending reset password mail.'}
            return jsonify_with_args(self.response_obj, 400)


class Verification(Resource):
    """
    临时验证
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def post(self):
        json_data = request.json
        email = json_data.get('email')
        captcha = json_data.get('captcha')
        if all([email, captcha]):
            ret_code = auth_ctrl.verify_temporary_pw(email, captcha)
            if ret_code:
                self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}
                return jsonify_with_args(self.response_obj, 200)
            elif ret_code is None:
                self.response_obj = {'status': '410', 'success': False, 'code': 0, 'data': None,
                                     'msg': 'Verification expire.'}
                return jsonify_with_args(self.response_obj, 200)
            else:
                self.response_obj = {'status': '409', 'success': False, 'code': 0, 'data': None,
                                     'msg': 'Verification error.'}
                return jsonify_with_args(self.response_obj, 200)
        else:
            self.response_obj = {'success': False, 'code': 1, 'data': None, 'msg': 'Need more args.'}
            return jsonify_with_args(self.response_obj, 400)
