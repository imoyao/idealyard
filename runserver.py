#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from back import create_app, setting

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    host_ip = setting.HOST_IP
    app.run(host=host_ip)  # TODO:此处需要写进环境变量
