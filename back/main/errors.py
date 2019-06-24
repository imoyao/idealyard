#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

from back.api_1_0 import api
from . import bp


class ValidationError(ValueError):
    pass


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def method_not_allowed(message):
    response = jsonify({'error': 'method not allowed', 'message': message})
    response.status_code = 405
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@bp.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response
