#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from werkzeug.utils import import_string

from back.api_1_0 import api, auth, posts, users, tags, archives, categories
from back.config import config
# from .api_1_0.books import Books
from .models import db

BLUEPRINTS = [
    'mains:bp',  # add bp here
    'api_1_0:api_bp',
]

cors = CORS(resources=r'/*')


def add_api():
    """
    添加 api 接口
    :return:
    """
    # api.add_resource(Books, '/api/books', '/api/books/<string:book_id>', )
    api.add_resource(auth.Auth, '/api/signin', '/api/token')
    api.add_resource(auth.ResetPassword, '/api/password')
    api.add_resource(posts.PostApi, '/api/articles')
    api.add_resource(posts.PostDetail, '/api/articles/<int:post_id>')
    api.add_resource(tags.TagApi, '/api/tags', '/api/tags/<int:tag_id>')
    api.add_resource(categories.CategoryApi, '/api/categories', '/api/categories/<int:category_id>')
    # api.add_resource(tags.TagDetail, '/api/tags/<int:post_id>')
    api.add_resource(archives.Archives, '/api/archives')
    # api.add_resource(archives.ArchivesDetail, '/api/archives/<int:post_id>')
    api.add_resource(users.CGUser, '/api/register', '/api/users/<int:user_id>')

    # api.add_resource(Setpwd, '/api/setpwd', )


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
    # db.drop_all()
    db.create_all(app=app)
