#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/30 8:38

from sqlalchemy import func, extract, and_

from back.models import db, Article
from back.utils import DateTime

date_maker = DateTime()
"""
归档：
先找出年份最大和最小值 >>> 按年划分
再找出每一年的按月划分 >> range(0,13)
"""


def last_create_time():
    """
    最晚创建时间
    :return:
    """
    last_time = db.session.query(func.max(Article.create_date).label('max_time')).one().max_time
    year = date_maker.year(last_time)
    return year


def first_create_time():
    """
    最早创建时间
    :return:
    """
    first_time = db.session.query(func.min(Article.create_date).label('min_time')).one().min_time
    first_year = date_maker.year(first_time)
    return first_year


def extract_post_with_year_and_month():
    """
    按照年、月筛选博文
    :return:
    """
    first = first_create_time()
    last = last_create_time()
    post_info_by_ct = []
    if all([first, last]):
        for year in range(first, last + 1):
            year_data = extract_post_with_month(year)
            post_info_by_ct.extend(year_data)
    return post_info_by_ct


def extract_post_with_month(year):
    same_year_data = []
    for mon in range(1, 13):
        ym = dict()
        post_obj = Article.query.filter(and_(
            extract('year', Article.create_date) == year,
            extract('month', Article.create_date) == mon
        )).all()
        same_month_posts = []
        if post_obj:
            for post in post_obj:
                data_item = dict()
                data_item['post_id'] = post.post_id
                str_date = ''
                create_date = post.create_date
                if create_date:
                    str_date = date_maker.make_strftime(create_date)
                data_item['create_date'] = str_date
                same_month_posts.append(data_item)
        # 没有博文，跳出本次循环
        else:
            continue
        ym['year'] = year
        ym['month'] = mon
        ym['posts'] = same_month_posts
        ym['counts'] = len(same_month_posts)
        same_year_data.append(ym)
    return same_year_data
