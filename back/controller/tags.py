#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:23
import json

from flask import g, jsonify, request
from flask import url_for, current_app
from flask_restful import Resource

from back import setting

from back.models import Tag
from back.controller import posts

from back.models import db, Article, posts_tags_table


def tag_info_json():
    pass


def tag_detail():
    pass


def query_tag_item(limit_count):
    """
    首先根据文章查询到各自的标签；
    然后对数据组装，放到一个字典中，没有则count=1,存在则count+=1；
    :param limit_count:
    :return: dict
    """
    '''
    {'Python': {'count': 1, 'id': 1}, '原创': {'count': 5, 'id': 8}, '后端': {'count': 1, 'id': 9}, '杂文': {'count': 3, 'id': 5}, 'MySQL': {'count': 1, 'id': 4}}
    '''
    article_obj = Article.query.limit(limit_count).all()
    tag_info = {}
    for post in article_obj:
        post_id = post.post_id
        tags = posts.tags_for_post(post_id)
        for tag in tags:
            if tag['tag_name'] not in tag_info:
                tag_info[tag['tag_name']] = {}
                tag_info[tag['tag_name']]['count'] = 1
            else:
                tag_info[tag['tag_name']]['count'] += 1
            tag_info[tag['tag_name']]['id'] = tag['id']
    return tag_info


def sort_tags(unsorted_dict, reverse=True):
    """
    排序
    :param unsorted_dict:
    :param reverse:
    :return:
    """
    return sorted(unsorted_dict.items(), key=lambda item: item[1]['count'], reverse=reverse)


def makeup_tag_item_for_index(tags):
    """
    json数据压缩成一层
    :param tags:
    :return:
    """
    return [{'tagname': info[0], 'count': info[1]['count'], 'id': info[1]['id']} for info in tags]


def show_all_tags():
    data = []
    tags = Tag.query.order_by(Tag.id).all()
    for data_obj in tags:
        tag = dict()
        tag['id'] = data_obj.id
        tag['tagname'] = data_obj.tag_name
        data.append(tag)
    return data


def posts_for_tag(tag_id):
    tag_obj = Tag.query.filter(Tag.id == tag_id).first()
    articles = tag_obj.articles
    print('-------', articles)
    tag_id = tag_obj.id
    tag_name = tag_obj.id
    return [{'id': tag_id, 'tagname': tag_name, 'articles': art.post_id} for art in articles]
