#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/4 15:10

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
# 注意此处命名，上为bp,下为api
api = Api()
