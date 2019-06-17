#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import abort, current_app, jsonify
from jinja2 import TemplateNotFound

from . import bp


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
