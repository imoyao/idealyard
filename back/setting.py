# -*- coding: utf-8 -*-
"""
该文件设置所有全局变量
"""
import os

LIMIT_NEW_POST_COUNT = 5
LIMIT_HOT_POST_COUNT = 5
LIMIT_HOT_TAG_COUNT = 10
INITIAL_VIEW_COUNTS = 0
INITIAL_POST_IDENTIFIER = 19930126
# 临时密码有效期
TEMPORARY_PW_EXPIRE_MINUTES = 10  # min
TEMPORARY_PW_EXPIRE_SECONDS = 60 * TEMPORARY_PW_EXPIRE_MINUTES  # second
# log
APP_LOG_FP = 'logs/app.log'
# flask
FLASK_HOST = '0.0.0.0'
FLASK_PORT = '5000'
HOST_IP = os.getenv('FLASK_HOST', FLASK_HOST)

# regex
RE_SYMBOL = r'[\,\，\.\。\?\？\:\：\'\‘\’\"\“\”\、\/\*\&\$\#\@\!\(\（\)\）\[\【\]\】\{\}\|\-"]'
RE_EXCLUDE_CHINESE = r'[A-Za-z0-9\!\%\[\]\,\。]'
