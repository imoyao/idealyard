#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/19 9:46
"""
Celery 从 4.0 开始启用新的小写配置名，某些配置被新的名称替换。
虽然旧的大写配置仍然支持，但如果你打算使用小写配置名，或是打算在未来进行迁移，
这里的配置加载方式就会失效，因为 Flask 在从文件或对象导入配置时只会导入大写形式的配置变量。
"""
from kombu import Exchange, Queue
broker_url = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379/1'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['application/json']
timezone = 'Asia/Shanghai'
enable_utc = True
celery_imports = ("tasks",)
broker_transport_options = {'visibility_timeout': 43200}
# 创建exchange
# see also: https://www.cnblogs.com/julyluo/p/6265775.html
default_exchange = Exchange('default', type='direct')
mail_exchange = Exchange('mail', type='direct')

task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('mail', mail_exchange, routing_key="mail")
)

task_default_queue = "default"
# see also:https://www.jianshu.com/p/b3d2c5871bec
# task_routes = {
#     'tasks.mem_test_long_task': {
#         'queue': 'mail',
#         'routing_key': 'mail',
#     },
#     'tasks.mem_bench_long_task': {
#         'queue': 'mail',
#         'routing_key': 'mail',
#     },
# }
