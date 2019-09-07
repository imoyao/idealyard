#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://www.pythondoc.com/flask/config.html#id6
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MPk2WlUArcLeeU_iohzT'  # TODO:set while production

    '''
    # 旧版本
    import random
    import string
    ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    # py3.6+
    import secrets
    secrets.token_urlsafe(nbytes=15)
    '''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # 分页
    FLASKY_POSTS_PER_PAGE = 10
    # 上传图片
    UPLOADED_IMAGES_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    # 邮件服务器设置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    # 163不支持STARTTLS
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('别院牧志', os.getenv('MAIL_USERNAME'))
    # redis 配置
    # REDIS_URL = "redis://:password@localhost:6379/0"
    REDIS_URL = "redis://localhost:6379/0"

    # REDIS_HOST = 'localhost'
    # REDIS_PORT = 6379
    # REDIS_DB = 0
    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class MySQLConfig:
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '111111'
    MYSQL_HOST = 'localhost:3306'
    MYSQL_CHARSET = 'utf8mb4'  # 为了支持 emoji 显示，需要设置为 utf8mb4 编码


class DevelopmentConfig(Config):
    DEBUG = True
    database = 'iyblog_dev'
    # 1366, "Incorrect string value: '\\xF0\\x9F\\x98\\x83</...' for column 'content_html' at row 1"
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
                              f'@{MySQLConfig.MYSQL_HOST}/{database}?charset={MySQLConfig.MYSQL_CHARSET}'


class TestingConfig(Config):
    TESTING = True
    database = 'iyblog_test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, database)


class ProductionConfig(Config):
    database = 'iyblog_product'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, database)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
