#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://www.pythondoc.com/flask/config.html#id6
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'WvCANWU9CiUTI6pm0wK6'  # TODO:set while production

    '''
    # py3.6+
    ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    # or
    import secrets
    secrets.token_urlsafe(nbytes=15)
    '''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class MySQLConfig:
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '111111'
    MYSQL_HOST = 'localhost:3306'


class DevelopmentConfig(Config):
    DEBUG = True
    database = 'mysql_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(MySQLConfig.MYSQL_USERNAME,
                                                                                MySQLConfig.MYSQL_PASSWORD,
                                                                                MySQLConfig.MYSQL_HOST, database)


class TestingConfig(Config):
    TESTING = True
    database = 'mysql_test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, database)


class ProductionConfig(Config):
    database = 'mysql_product'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, database)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
