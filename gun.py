#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/7 15:40

import os
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

from back import setting

if not os.path.exists('logs'):
    os.mkdir('logs')
debug = True
loglevel = 'debug'
# 绑定的ip及端口号
app_host = setting.FLASK_HOST
app_port = setting.FLASK_PORT
bind = ':'.join([app_host, app_port])

pidfile = 'gunicorn.pid'
logfile = '/var/log/app/debug.log'

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 使用gevent模式
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
# 项目的根目录,比如你的app.py文件在/home/ubuntu/app目录下，就填写'/home/ubuntu/app'
# chdir = ''

x_forwarded_for_header = 'X-FORWARDED-FOR'
