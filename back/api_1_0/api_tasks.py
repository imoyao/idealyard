#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/9/8 12:21
from flask import jsonify
from flask_restful import Resource

from back.celery_components import tasks as celery_tasks


class TaskStatus(Resource):
    """
    获取状态
    see also:http://www.pythondoc.com/flask-celery/first.html
    """

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'info': {}, 'msg': ''}

    def get(self, task_id, name):
        task = None
        if name == 'mail':
            task = celery_tasks.send_reset_password_mail_long_task.AsyncResult(task_id)
        elif name == 'membench':
            pass
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'result': task.result,
            }
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.get()),  # this is the exception raised
            }

        self.response_obj['info'] = response
        return jsonify(self.response_obj)
