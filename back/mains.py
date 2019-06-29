#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 8:01


from flask import Blueprint
from flask import abort, current_app, jsonify
from jinja2 import TemplateNotFound

bp = Blueprint('main', __name__)


@bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')


@bp.route('/')
@bp.route('/index/')
def index():
    try:
        return 'This is Index Page.'
    except TemplateNotFound:
        abort(404)


@bp.route('/ping')
def ping_pong():
    return jsonify('pong!')


@bp.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response


@bp.app_errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response
