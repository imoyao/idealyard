#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/8 18:30
"""
调度任务
cd CURRENT_APP_PATH
celery -A celery_worker:celery worker --loglevel=DEBUG -f /var/log/celery/celery.log
主要参考：
https://github.com/nebularazer/flask-celery-example
https://github.com/chiqj/flask-with-celery-example
https://github.com/zenyui/celery-flask-factory
"""
import os

from celery.schedules import crontab

from back import create_app
from back.celery_components import tasks
from back.celery_components import init_celery

flask_app = create_app(os.getenv('FLASK_CONFIG', 'default'))
celery = init_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    周期性任务
    # 添加定时任务参见：https://www.cnblogs.com/linxiyue/archive/2017/12/21/8082102.html
    :param sender:
    :param kwargs:
    :return:
    """
    # sender.add_periodic_task(10.0, tasks.write_bmc_power_state_to_db,
    #                          name='write_bmc_power_state_to_db every 10s')

    # sender.add_periodic_task(3000.0, tasks.my_add(2, 3), name='my_add every 5min')

    # Calls log('Logging Stuff') every 30 seconds
    sender.add_periodic_task(300.0, tasks.log.s('Logging Stuff'), name='Log every 300s')
    # sender.add_periodic_task(30.0, tasks.send_reset_password_mail_long_task('0.0.0.0', 'emailme8@163.com'),
    #                          name='my_add every 5min')

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        tasks.log.s('Monday morning log!'),
    )
