#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import abort, current_app, render_template, jsonify
from jinja2 import TemplateNotFound

from . import main_bp


@main_bp.route('/hello')
def hello_world():
    return 'Hello World!'


@main_bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')


@main_bp.route('/')
@main_bp.route('/index/')
def index():
    try:
        return 'This is Index Page.'
        # return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/ping')
def ping_pong():
    return jsonify('pong!')
