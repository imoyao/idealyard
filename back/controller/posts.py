#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:18
import random
from flask import g
from sqlalchemy import func

from back import setting
from back.controller import QueryComponent, MakeupPost, MakeQuery, assert_new_tag_in_tags
from back.controller import categories, tags
from back.models import ArticleBody, Article, Tag, db
from back.utils import DateTime

date_maker = DateTime()


class GetPostCtrl:

    @staticmethod
    def posts_order_by_date(desc=True):
        if desc:
            posts_query = Article.query.order_by(Article.create_date.desc())
        else:
            posts_query = Article.query.order_by(Article.create_date)
        return posts_query

    @staticmethod
    def posts_order_by_view_counts(desc=True):
        if desc:
            posts_query = Article.query.order_by(Article.view_counts.desc())
        else:
            posts_query = Article.query.order_by(Article.view_counts)
        return posts_query

    @staticmethod
    def make_limit(query_data, limit_count):
        """
        是否对数量限制
        :param query_data:
        :param limit_count:
        :return:
        """
        if limit_count >= 1:
            posts = query_data.limit(limit_count).all()
        else:
            posts = query_data.all()
        data = MakeupPost.post_info_json(posts)
        return data

    @staticmethod
    def make_paginate(query_data, page=None, per_page=None):
        """
        返回分页对象
        :param query_data:
        :param page:
        :param per_page:
        :return:
        """
        assert all([page, per_page])
        pagination = query_data.paginate(
            page, per_page=per_page, error_out=False
        )
        return pagination

    @staticmethod
    def post_detail(post_info):
        """
        用户点击文章链接跳详情页的数据接口，返回在这里找
        :param post_info:
        :return:
        """
        user_id = post_info.author_id
        body_id = post_info.body_id
        category_id = post_info.category_id
        post_id = post_info.post_id
        post_identifier = post_info.identifier
        create_date = post_info.create_date
        user_info = QueryComponent.author_info_for_post(user_id)
        body_info = QueryComponent.content_for_post(body_id)
        category_info = QueryComponent.category_for_post(category_id)
        tags_info = QueryComponent.tags_for_post(post_id)['tags_info']
        str_date = ''
        if create_date:
            str_date = date_maker.make_strftime(create_date)
        json_post = {
            "author": user_info,
            "body": body_info,
            "category": category_info,
            # TODO:后期添加
            "commentCounts": 0,
            "createDate": str_date,
            "id": post_id,
            "identifier": post_identifier,
            # TODO:摘要，暂无；感觉这个api不需要该参数？？？
            # "summary": "本节将介绍如何在项目中使用 Element。",
            "tags": tags_info,
            "title": post_info.title,
            "viewCounts": post_info.view_counts,
            "weight": post_info.weight,
        }
        return json_post

    def get_post_detail_by_args(self, query_by, order_by, category_id, tag_id, year, month, new=False, hot=False,
                                order_by_desc=True):
        """
        根据各种条件查询文章
        :param query_by: str,查询字段:item in ['category','tag','archive']
        :param order_by: 排序字段
        :param category_id: int,分类id
        :param tag_id: int, 标签id
        :param year: int, 年份
        :param month: int,月份
        :param new: bool
        :param hot: bool
        :param order_by_desc: bool
        :return:
        """
        query_data = None
        queryed = False
        if query_by:
            if query_by == 'category':
                query_data = MakeQuery.query_category(category_id)
            elif query_by == 'tag':
                queryed = True
                query_data = MakeQuery.query_post_by_tag_of(tag_id, order_by=order_by, desc=order_by_desc)
            elif query_by == 'archive':
                queryed = True
                query_data = MakeQuery.order_archive(year, month, order_by=order_by, desc=order_by_desc)
            else:
                queryed = True
                pass
        # ?new=true&limit=5
        if not queryed:
            if new or order_by == 'create_date':
                query_data = self.posts_order_by_date(desc=order_by_desc)
            # ?hot=true&limit=5
            elif hot or order_by == 'view_counts':
                query_data = self.posts_order_by_view_counts(desc=order_by_desc)
        return query_data


class PostNewArticle:
    # TODO: 其他 controllers 也应该这么写
    """
    创建新博文
    """

    @staticmethod
    def new_post_body(summary, content_html, content):
        body = ArticleBody(summary=summary, content=content, content_html=content_html)
        db.session.add(body)
        db.session.commit()
        return body.id

    @staticmethod
    def gen_post_identifier():
        """
        生成新的文章标识码
        规则：找到现有最大值，然后加随机数
        :return: int
        """
        # (19930126,)[0]
        max_identifier = db.session.query(func.max(Article.identifier)).one_or_none()
        if max_identifier:
            max_num = max_identifier[0]
            increase_int = random.randrange(1, 5)
            post_identifier = max_num + increase_int
        else:
            post_identifier = setting.INITIAL_POST_IDENTIFIER
        return post_identifier

    def new_post_action(self, category_id, all_tags_for_new_post, title, body_id, weight=0):
        """
        添加一篇博文
        :param category_id: int,
        :param all_tags_for_new_post: list
        :param title: str,
        :param body_id: int
        :param weight:
        :return:
        """
        new_identifier = self.gen_post_identifier()
        print('-----g.user.id------', g)
        # print('-----g.user.id------', g.user.id)
        author_id = '1'  # TODO: just for test
        post = Article(title=title, identifier=new_identifier, author_id=author_id, body_id=body_id,
                       view_counts=setting.INITIAL_VIEW_COUNTS,
                       weight=weight, category_id=category_id)
        print('-----all_tags_for_new_post', all_tags_for_new_post)
        need_add_tags = assert_new_tag_in_tags(all_tags_for_new_post)
        # TODO:正常函数不应该走到这里，因为前面已经添加了用户自主添加的，此处主要是刚开始写的代码不完善
        if need_add_tags:
            tags.new_multi_tags(need_add_tags)
        for tag_name in all_tags_for_new_post:
            # tag_obj = Tag.query.filter_by(tag_name=tag_name).first()
            # TODO: next line is right
            tag_obj = Tag.query.filter_by(tag_name=tag_name).one()
            post.tags.append(tag_obj)

        db.session.add(post)
        db.session.commit()
        post_id = post.post_id
        print('post_id', 'post_id')
        return post_id

    def new_post(self, category_name, summary, content_html, content, title, weight=0, category_description='',
                 post_tags=None,
                 category_id=None):
        """
        POST 博文，需要先看是否要 POST category、tag；然后 POST body；最后操作 Article 表
        :param category_name:str,
        :param category_description:str,
        :param summary:str,
        :param content_html:str,
        :param content:str,
        :param title:str,
        :param weight:int #TODO:bool? int?
        :param post_tags:list,
        :param category_id:int,
        :return:int,new_post_id
        """
        all_tags_for_new_post = None

        if not category_id and category_name:
            category_id = categories.new_category(category_name, category_description)

        if post_tags:
            all_tags_for_new_post = tags.add_tag_for_post(post_tags)

        body_id = self.new_post_body(summary, content_html, content)

        new_post_id = self.new_post_action(category_id, all_tags_for_new_post, title, body_id, weight=weight)

        return new_post_id
