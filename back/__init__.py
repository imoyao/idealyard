#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class

from back.api_1_0 import api, auth, posts, users, tags, archives, categories, comments, users, uploads, api_tasks
from back.config import config
from .api_1_0.books import Books, Test
from .models import db
from back.api_1_0 import api_bp
from back.main import main_bp
from back.utils.flask_logger import register_logger
from back.utils.mail import mail
from back.utils.redis_util import redis_store

cors = CORS(resources={r"/api/*": {"origins": "*"}})


def add_api():
    """
    添加 api 接口
    :return:
    """
    api.add_resource(Test, '/api/tests', '/api/books/<string:book_id>')

    api.add_resource(auth.Auth, '/api/signin', '/api/token')
    api.add_resource(auth.ResetPassword, '/api/password')
    api.add_resource(auth.EmailApi, '/api/emails')
    api.add_resource(auth.Verification, '/api/verifications')
    api.add_resource(users.UserApi, '/api/register', '/api/users', '/api/users/<int:user_id>')

    api.add_resource(posts.PostApi, '/api/articles')
    api.add_resource(posts.PostDetail, '/api/articles/<int:post_id>')
    api.add_resource(posts.IdentifyPostDetail, '/api/identifiers/<int:identifier>')
    api.add_resource(posts.SlugApi, '/api/slugs')
    api.add_resource(posts.IdApi, '/api/identifiers')
    api.add_resource(tags.TagApi, '/api/tags', '/api/tags/<int:tag_id>')
    api.add_resource(categories.CategoryApi, '/api/categories', '/api/categories/<int:category_id>')
    # api.add_resource(tags.TagDetail, '/api/tags/<int:post_id>')
    api.add_resource(archives.Archives, '/api/archives')
    api.add_resource(comments.Comments, '/api/comments', '/api/tags/<int:comment_id>')

    # api.add_resource(archives.ArchivesDetail, '/api/archives/<int:post_id>')
    api.add_resource(uploads.UploadImage, '/api/images')
    api.add_resource(api_tasks.TaskStatus, '/api/tasks/<string:task_id>/<string:name>')


def add_blueprints(app):
    """
    添加蓝图
    :param app:
    :return:
    """
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)


def create_app(config_name):
    # app = Flask(__name__, static_folder="../static", template_folder="..")
    app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # Load extensions
    register_logger(__name__)
    cors.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)  # 在db对象创建之后调用！
    configure_uploads(app, uploads.image_upload)  # configure_uploads(app, [files, photos])
    mail.init_app(app)
    redis_store.init_app(app)
    patch_request_class(app, size=None)  # 防止用户上传过大文件导致服务器空间不足，加此自动引发HTTP错误。
    add_api()
    # api.init_app需要写在add_api()之后
    api.init_app(app)
    # Load blueprints
    add_blueprints(app)
    return app


def init_db(app):
    """
    初始化db
    :return:
    """
    # db.drop_all()
    db.create_all(app=app)
