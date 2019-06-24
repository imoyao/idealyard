#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

from . import bp


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
