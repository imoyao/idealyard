#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/31 21:00
# https://stackoverflow.com/questions/30040159/why-use-flasks-redis-extension
from flask_redis import FlaskRedis

from redis import StrictRedis

redis_store = FlaskRedis.from_custom_provider(StrictRedis)
