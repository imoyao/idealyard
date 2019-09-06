# -*- coding:utf-8 -*-
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from back import setting


def register_logger(name):
    # 改进：http://maqiangthunder.github.io/2016/04/18/python/flask/flask%E7%B3%BB%E7%BB%9F%E6%97%A5%E5%BF%97%E5%86%99%E5%88%B0%E6%96%87%E4%BB%B6/
    logger = logging.getLogger(name)
    dir_name, _ = os.path.split(setting.APP_LOG_FP)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    logger.setLevel(logging.INFO)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)-2s[%(name)s]: %(message)s')
    # 文件日志
    file_handler = RotatingFileHandler(setting.APP_LOG_FP, maxBytes=10 * 1024 * 1024, backupCount=7)
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    # logger.setLevel(logging.DEBUG)
    return logger
