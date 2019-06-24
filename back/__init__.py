#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.utils import import_string

from .config import config
from .api_1_0.auth import Auth
# from .api_1_0.books import Books
from .api_1_0.setpwd import Setpwd
from .models import db

BLUEPRINTS = [
    'main:bp',  # add bp here
    # 'tools:bp',
    # 'settings:bp',
    'api_1_0:api',
]

cors = CORS(resources=r'/*')
api = Api()


def add_api():
    """
    添加 api 接口
    :return:
    """
    # api.add_resource(Books, '/api/books', '/api/books/<string:book_id>', )
    api.add_resource(Auth, '/api/login', )
    api.add_resource(Setpwd, '/api/setpwd', )


def create_app(config_name):
    app = Flask(__name__, static_folder="../static", template_folder="..")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # Load extensions
    cors.init_app(app)
    db.init_app(app)
    add_api()
    # api.init_app需要写在add_api()之后
    api.init_app(app)
    # Load blueprints
    for bp_name in BLUEPRINTS:
        bp = import_string(bp_name)
        app.register_blueprint(bp)
    return app


def init_db(app):
    """
    初始化db
    :return:
    """
    db.create_all(app=app)
