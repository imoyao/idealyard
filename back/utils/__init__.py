#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/16 10:04
import hashlib


def md5_encrypt(origin_str):
    """
    md5加密
    :param origin_str:
    :return:
    """
    _m1 = hashlib.md5()
    # 此处必须声明encode,若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    _m1.update(origin_str.encode(encoding='utf-8'))
    _rtn = _m1.hexdigest()
    return _rtn
