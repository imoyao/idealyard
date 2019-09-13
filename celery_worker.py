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

from back import setting
from back.celery_components import tasks
from back.celery_components import celery_app

celery = celery_app


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

    sender.add_periodic_task(300.0, tasks.send_backup_data_mail(setting.SEND_BACKUP_TO_MAIL),
                             name='send_backup_data_mail every 1 min.')

    # Calls log('Logging Stuff') every 30 seconds
    sender.add_periodic_task(60 * 60, tasks.log.s('Logging Stuff'), name='Log every an hour.')

    # Executes every Monday morning at 10:00 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=0, day_of_week=1),
        tasks.send_backup_data_mail(setting.SEND_BACKUP_TO_MAIL),
        name='Send mail Monday of every week.'
    )
