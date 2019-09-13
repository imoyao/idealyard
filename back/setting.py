# -*- coding: utf-8 -*-
"""
该文件设置所有全局变量
"""
import os
import sys

from back import config

LIMIT_NEW_POST_COUNT = 5
LIMIT_HOT_POST_COUNT = 5
LIMIT_HOT_TAG_COUNT = 10
INITIAL_VIEW_COUNTS = 0
INITIAL_POST_IDENTIFIER = 19930126
# 临时密码有效期
TEMPORARY_PW_EXPIRE_MINUTES = 10  # min
TEMPORARY_PW_EXPIRE_SECONDS = 60 * TEMPORARY_PW_EXPIRE_MINUTES  # second
# user info
SEND_BACKUP_TO_MAIL = 'emailme8@163.com'        # TODO：用户备份邮箱
# fp
APP_LOG_FP = 'logs/app.log'
BACK_UP_DATA_FP = 'back/data/backup'
BACKUP_PREFIX = 'backup_'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# flask
FLASK_HOST = '0.0.0.0'
FLASK_PORT = '5000'
HOST_IP = os.getenv('FLASK_HOST', FLASK_HOST)
# baidu_trans
BD_TRANS_API_URL = '/api/trans/vip/translate'
# db
DB_HOST = 'localhost'
DB_USER = 'root'            # TODO:export this
DB_PASSWORD = '111111'
config_name = os.getenv('FLASK_CONFIG', 'default')
print(config_name,'----------------config_name')
DATABASE_NAME = 'iyblog_dev'
print(DATABASE_NAME,'-------DATABASE_NAME---------config_name')
# regex
RE_SYMBOL = r'[\,\，\.\。\?\？\:\：\'\‘\’\"\“\”\、\/\*\&\$\#\@\!\(\（\)\）\[\【\]\】\{\}\|\-"]'
RE_EXCLUDE_CHINESE = r'[A-Za-z0-9\!\%\[\]\,\。]'
