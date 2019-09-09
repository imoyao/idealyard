#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/19 9:45
"""
分离出来的原因：https://www.v2ex.com/t/471458
"""
import os

from celery import Celery
from back.celery_components import celery_config

# from back import create_app
#
# flask_app = create_app(os.getenv('FLASK_CONFIG', 'default'))


def init_celery(app=None):
    """
    初始化celery
    参见：http://docs.jinkan.org/docs/flask/patterns/celery.html
    :return:
    """
    celery = Celery(__name__, broker=celery_config.broker_url, backend=celery_config.result_backend)
    celery.config_from_object('back.celery_components.celery_config')
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
