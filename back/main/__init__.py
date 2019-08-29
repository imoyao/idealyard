#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

main_bp = Blueprint('main', __name__)

from . import views, errors
