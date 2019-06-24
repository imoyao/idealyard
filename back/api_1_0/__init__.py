#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/4 15:10

from flask import Blueprint

api = Blueprint('api', __name__)

from . import books, auth, setpwd
