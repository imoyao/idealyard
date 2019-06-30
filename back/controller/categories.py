#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 22:28
from sqlalchemy import func, extract, and_
from back.models import db, Article, Category
"""
分类 按照类别分组
"""




def category_year_month():
    category_obj = Category.query.all()
    pass

    [
        {
            "commentCounts": 0,
            "count": 1,
            "month": 1,
            "summary": "",
            "title": "",
            "viewCounts": 0,
            "weight": 0,
            "year": 2018
        },
        {
            "commentCounts": 0,
            "count": 2,
            "month": 2,
            "summary": "",
            "title": "",
            "viewCounts": 0,
            "weight": 0,
            "year": 2018
        },
        {
            "commentCounts": 0,
            "count": 2,
            "month": 11,
            "summary": "",
            "title": "",
            "viewCounts": 0,
            "weight": 0,
            "year": 2018
        },
        {
            "commentCounts": 0,
            "count": 2,
            "month": 2,
            "summary": "",
            "title": "",
            "viewCounts": 0,
            "weight": 0,
            "year": 2019
        }
    ],
