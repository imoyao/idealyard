# -*- coding: utf-8 -*-
"""
该文件设置所有全局变量
"""

LOGINUSER = ''
LIMIT_NEW_POST_COUNT = 5
LIMIT_HOT_POST_COUNT = 5
LIMIT_HOT_TAG_COUNT = 10
INITIAL_VIEW_COUNTS = 0
INITIAL_POST_IDENTIFIER = 19930126
# log
APP_LOG_FP = 'logs/app.log'

# regex
RE_SYMBOL = r'[\,\，\.\。\?\？\:\：\'\‘\’\"\“\”\、\/\*\&\$\#\@\!\(\（\)\）\[\【\]\】\{\}\|\-"]'
RE_EXCLUDE_CHINESE = r'[A-Za-z0-9\!\%\[\]\,\。]'