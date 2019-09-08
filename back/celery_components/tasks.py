#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/18 16:24
"""
存放需要异步执行的耗时任务
"""

import random
import time

from celery import Celery
# from celery.signals import task_postrun
from celery.utils.log import get_task_logger
# from flask_mail import Message

# from back.models import db
from back.controller.authctrl import PostUserCtrl

# from back.utils.mail import mail as mail_app
# from . import flask_app

auth_ctrl = PostUserCtrl()

# https://blog.csdn.net/qq_27437781/article/details/83507110
logger = get_task_logger(__name__)

celery = Celery('tasks')


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


# @celery.task
# def send_async_reset_pw_email(req_ip, verify_email):
#     """
#     Background task to send an email with Flask-Mail.
#     :param req_ip: str，
#     :param verify_email: str,接受者
#     :return:
#     """
#     captcha = auth_ctrl.gen_captcha()
#     hash_pw = auth_ctrl.hash_temporary_pw(captcha)
#     set_success = auth_ctrl.set_temporary_pw(verify_email, hash_pw)
#     if set_success:
#         email_data = auth_ctrl.makeup_send_reset_pw_mail(req_ip, captcha)
#         msg = Message(email_data['subject'],
#                       sender=flask_app.config['MAIL_DEFAULT_SENDER'],
#                       recipients=[verify_email])
#         msg.body = email_data['body']
#         with flask_app.app_context():
#             mail_app.send(msg)


@celery.task(bind=True)  # 添加了 bind=True 参数。这个参数告诉 Celery 发送一个 self 参数到我的函数，我能够使用它(self)来记录状态更新。
def send_reset_password_mail_long_task(self, req_ip, email):
    """
    发送验证邮件
    :param self:
    :param req_ip:
    :param email:
    :return:
    """
    try:
        print((req_ip, email), '----------------1111111111')
        ret = auth_ctrl.reset_pw_action(req_ip, email)
        print(ret, '------------------1111')
    except Exception as exc:
        print(exc, '-----------------------')
        raise self.retry(countdown=60 * 5, exc=exc)
    return ret


@celery.task
def log(message):
    """Print some log messages"""
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


# @task_postrun.connect
# def close_session(*args, **kwargs):
#     # Flask SQLAlchemy will automatically create new sessions for you from
#     # a scoped session factory, given that we are maintaining the same app
#     # context, this ensures tasks have a fresh session (e.g. session errors
#     # won't propagate across tasks)
#     db.session.remove()


@celery.task()
def log_it(num1, num2):
    msg = num1 + num2
    print(msg)
    logger.debug("in log_test()")
    return msg


if __name__ == '__main__':
    task = log_it.apply_async(args=[10, 20], countdown=10)
