#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/18 16:24
"""
存放需要异步执行的耗时任务
https://segmentfault.com/a/1190000008022050
"""

import random
import time

# from celery.signals import task_postrun
from celery.utils.log import get_task_logger

from back.controller.authctrl import PostUserCtrl
from back.controller.backup import BackupCtrl

from back.celery_components import celery_app

# https://blog.csdn.net/qq_27437781/article/details/83507110
logger = get_task_logger(__name__)
auth_ctrl = PostUserCtrl()
backer = BackupCtrl()


@celery_app.task(bind=True)
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


# 添加了 bind=True 参数。这个参数告诉 Celery 发送一个 self 参数到我的函数，我能够使用它(self)来记录状态更新。
@celery_app.task(bind=True)
def send_reset_password_mail_long_task(self, req_ip, email):
    """
    发送验证邮件
    :param self:
    :param req_ip:
    :param email:
    :return:
    """
    ret = auth_ctrl.reset_pw_action(req_ip, email)
    return ret


@celery_app.task(bind=True)
def send_backup_data_mail(self, email):
    """
    发送备份文件，同时完成备份文件整理工作
    :param self:
    :param email:
    :return:
    """
    logger.info(f'send mail to {email}.')
    back_packages = backer.mail_back_up_action(email)
    logger.info(f'send mail to f---back_packages----------00000000000--- {back_packages}.')
    ret = backer.rename_and_remove_back_up(back_packages)
    logger.info(f'send mail to------ret------12335436-- f{ret}.')
    return ret


@celery_app.task
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


@celery_app.task()
def log_it(num1, num2):
    msg = num1 + num2
    print(msg)
    logger.debug("in log_test()")
    return msg


if __name__ == '__main__':
    task = log_it.apply_async(args=[10, 20], countdown=10)
