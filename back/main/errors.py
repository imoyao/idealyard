#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask import render_template

from . import main_bp


@main_bp.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response