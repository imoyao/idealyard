#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:23

from back.controller import posts
from back.models import Article
from back.models import Tag, db


def query_tag_item(limit_count):  # DEPRECATED
    """
    首先根据文章查询到各自的标签；
    然后对数据组装，放到一个字典中，没有则count=1,存在则count+=1；
    :param limit_count:
    :return: dict
    """
    '''
    {'Python': {'count': 1, 'id': 1}, '原创': {'count': 5, 'id': 8}, '后端': {'count': 1, 'id': 9}, '杂文': {'count': 3, 'id': 5}, 'MySQL': {'count': 1, 'id': 4}}
    '''
    if limit_count:
        article_obj = Article.query.limit(limit_count).all()
    else:
        article_obj = Article.query.all()
    tag_info = {}
    for post in article_obj:
        post_id = post.post_id
        tags = posts.tags_for_post(post_id)['tags_info']
        for tag in tags:
            if tag['tag_name'] not in tag_info:
                tag_info[tag['tag_name']] = {}
                tag_info[tag['tag_name']]['posts_count'] = 1
            else:
                tag_info[tag['tag_name']]['posts_count'] += 1
            tag_info[tag['tag_name']]['id'] = tag['id']
    return tag_info


def sort_tags(unsorted_dict, reverse=True):
    """
    按照标签下的文章 count 排序
    :param unsorted_dict:
    :param reverse:
    :return:
    """
    return sorted(unsorted_dict.items(), key=lambda item: item[1]['posts_count'], reverse=reverse)


def makeup_tag_item_for_index(tags):
    """
    json数据压缩成一层
    :param tags:
    :return:
    """
    return [{'tagname': info[0], 'count': info[1]['posts_count'], 'id': info[1]['id']} for info in tags]


def order_tags_by_post_id(desc=True):
    """
    按照tag id 排序
    :return:
    """
    if desc:
        tags_query = Article.query.order_by(Article.post_id.desc())
    else:
        tags_query = Article.query.order_by(Article.post_id)
    return tags_query


def show_all_tags():
    """
    查询所有的tag 信息 （一次全查）
    :return:
    """
    data = []
    tags = Tag.query.all()
    for data_obj in tags:
        tag = dict()
        # 文章id
        # TODO：hint:注意此处，遍历之后可以反查文章信息
        articles = [data.post_id for data in data_obj.articles]
        tag['id'] = data_obj.id
        tag['tagname'] = data_obj.tag_name
        tag['articles'] = articles
        tag['article_counts'] = len(data_obj.articles)
        data.append(tag)
    return data


def query_all_data():
    return Tag.query.all()


def posts_by_tag_id(tag_id):
    """
    根据 tag id 查找对应的文章信息（查指定的）
    :param tag_id: int,
    :return:dict,
    """
    tag_obj = Tag.query.filter(Tag.id == tag_id).first()
    posts_data = tag_obj.articles
    articles = []
    if posts_data:
        # 文章id列表
        articles = [data.post_id for data in posts_data]
    tag_id = tag_obj.id
    tag_name = tag_obj.tag_name
    data = {
        'id': tag_id,
        'tagname': tag_name,
        'articles': articles,
        'article_counts': len(articles),
    }
    return data


def make_tag_limit(query_data, limit_count):
    """
    是否对数量限制
    :param query_data:
    :param limit_count:
    :return:
    """
    if limit_count >= 1:
        # AttributeError: 'list' object has no attribute 'limit'
        data = query_data[:limit_count]
    else:
        data = query_data
    return data


def tags_of_post_counts(query_data, limit_count):  # TODO:与 show_all_tags()合并
    """
    获取各标签下文章个数
    :return:dict,like {TAG_NAME: {POSTS_COUNT: int, ID: int,TAG_NAME:str}, ……}
    """
    article_obj = make_tag_limit(query_data, limit_count)
    '''
    below equal this:
    return [{posts_by_tag_id(post.post_id)['tag_name']: posts_by_tag_id(post.post_id)['article_counts']} for post in article_obj]
    '''
    # 组装
    all_tags = {}
    if article_obj:
        for data_obj in article_obj:
            tag = dict()
            # 文章id
            # TODO：hint:注意此处，遍历之后可以反查文章信息
            articles = [data.post_id for data in data_obj.articles]
            tag_name = data_obj.tag_name
            tag['id'] = data_obj.id
            tag['tagname'] = data_obj.tag_name
            tag['articles'] = articles
            tag['posts_count'] = len(data_obj.articles)
            all_tags[tag_name] = tag
    return all_tags


def order_tags_by_include_post_counts(query_data, limit_count, desc=True):
    """
    按照标签热度排就是按照各标签下文章的个数排
    :param query_data:
    :param limit_count:
    :param desc:
    :return:
    """
    tags_info = tags_of_post_counts(query_data, limit_count)
    # 把列表展开放到字典中，因为标签是唯一的
    tags_sorted = sort_tags(tags_info, reverse=desc)
    data = makeup_tag_item_for_index(tags_sorted)
    return data


# ====POST====

def new_tag(tag_name):
    """
    添加单个tag
    :param tag_name: str,
    :return:str,tag_name
    """
    assert tag_name
    tag = Tag(tag_name=tag_name)
    db.session.add(tag)
    db.session.commit()
    return tag.tag_name


def new_multi_tags(tag_names):
    """
    添加多个标签
    :param tag_names:list/set,
    :return:list, [tag_name1,tags_name2,……]
    """
    assert not isinstance(tag_names, str)
    assert len(tag_names) >= 1
    tags = []
    for tag_item in tag_names:
        tags.append(new_tag(tag_item))
    return tags


def add_tag(post_tags):
    if post_tags:
        # 新增 tag 没有默认id,过滤拿到之后去 POST
        new_tags = []
        origin_tags = []
        new_add_tags = []
        for tag in post_tags:
            if not tag.get('id'):
                should_new_tags = tag.get('name') and tag['name']
                new_tags.append(should_new_tags)
            else:
                already_exist_tag = tag.get('name') and tag['name']
                origin_tags.append(already_exist_tag)

        if new_tags:
            new_add_tags = new_multi_tags(new_tags)
        all_tags_for_new_post = set(origin_tags) | set(new_add_tags)
        return all_tags_for_new_post


def add_tag_for_post(post_tags):
    assert not isinstance(post_tags, str)
    assert post_tags
    # 新增 tag 没有默认id,过滤拿到之后去 POST
    new_tags = []
    origin_tags = []
    new_add_tags = []
    for tag in post_tags:
        print('---332-----', tag)
        if not tag.get('id'):
            should_new_tags = tag.get('name') and tag['name']
            new_tags.append(should_new_tags)
        else:
            already_exist_tag = tag.get('name') and tag['name']
            origin_tags.append(already_exist_tag)

    if new_tags:
        new_add_tags = new_multi_tags(new_tags)
    all_tags_for_new_post = set(origin_tags) | set(new_add_tags)
    return all_tags_for_new_post
