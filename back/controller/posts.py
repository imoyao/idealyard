#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/29 15:18
import re
import json
import random
from multiprocessing import Value

from flask import abort
from sqlalchemy import func

from back import setting
from back.utils.text import BaiduTrans
from back.controller import QueryComponent, MakeupPost, MakeQuery, assert_new_tag_in_tags
from back.controller import categories, tags
from back.models import ArticleBody, Article, Tag, db
from back.utils.date import DateTime

date_maker = DateTime()
category_poster = categories.PostCategoryCtrl()
tag_poster = tags.PostTagCtrl()
query_maker = MakeQuery()


class GetPostCtrl:

    @staticmethod
    def posts_order_by_date(desc=True):
        """
        按照日期排序（weight为**置顶**功能<因为目前`weight`只是bool(1,0)型，所以desc是无用的，即置顶文章也是按照`create_date`排序的；但是如果需要的话，可以给每篇文章加权重，从而使文章置顶>）
        :param desc:
        :return:
        """
        if desc:
            posts_query = Article.query.order_by(Article.weight.desc(), Article.create_date.desc())
        else:
            posts_query = Article.query.order_by(Article.weight.desc(), Article.create_date)
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
        post_slug = post_info.slug
        create_date = post_info.create_date
        update_date = post_info.update_date
        user_info = QueryComponent.author_info_for_post(user_id)
        body_info = QueryComponent.content_for_post(body_id)
        category_info = QueryComponent.category_for_post(category_id)
        tags_info = QueryComponent.tags_for_post(post_id)['tags_info']
        str_date, str_ut = ('',) * 2
        if create_date:
            str_date = date_maker.make_strftime(create_date)
        if update_date:
            str_ut = date_maker.make_strftime(update_date)
        json_post = {
            "author": user_info,
            "body": body_info,
            "category": category_info,
            # TODO:后期添加
            "commentCounts": 0,
            "createDate": str_date,
            "updateDate": str_ut,
            "id": post_id,
            "identifier": post_identifier,
            "slug": post_slug,
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
        :param new: bool,
        :param hot: bool,
        :param order_by_desc: bool,
        :return:
        """
        query_data = None
        queryed = False
        if query_by:
            queryed = True
            if query_by == 'category':
                query_data = MakeQuery.query_post_by_category_of(category_id, order_by=order_by, desc=order_by_desc)
            elif query_by == 'tag':
                query_data = MakeQuery.query_post_by_tag_of(tag_id, order_by=order_by, desc=order_by_desc)
            elif query_by == 'archive':
                query_data = query_maker.order_archive(year, month, order_by=order_by, desc=order_by_desc)
            else:
                pass
        # ?new=true&limit=5
        if not queryed:
            if new or order_by == 'create_date':
                query_data = self.posts_order_by_date(desc=order_by_desc)
            # ?hot=true&limit=5
            elif hot or order_by == 'view_counts':
                query_data = self.posts_order_by_view_counts(desc=order_by_desc)
        return query_data


class PostArticleCtrl:
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
    def get_post_id_by_identifier(identifier, description=None):
        """
        如果有，则返回，如果没有，直接404
        :param identifier:
        :param description:
        :return:
        """
        post = Article.query.filter_by(identifier=identifier).one_or_none()
        if post is not None:
            return post.post_id
        abort(404, description=description)

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

    @staticmethod
    def parse_trans_en2cn(q_key, from_lang='auto', to_lang='en'):
        """
        根据用户输入关键字翻译，返回对应的英文字符串
        :param q_key: str,
        :param from_lang: str,default:auto
        :param to_lang: str,en
        :return: str, 中文所对应的的英文翻译
        """
        bd_trans = BaiduTrans(q_key, from_lang=from_lang, to_lang=to_lang)
        dst = ''
        _ret = bd_trans.trans_response()
        if _ret:
            # bytes >> str >> dict
            dict_ret = json.loads(_ret.decode())
            result = dict_ret.get('trans_result')
            if result:
                dst = result[0]['dst']
        return dst

    @staticmethod
    def make_up_slug(raw_slug):
        """
        in:You look great today!
        out:you-look-great-today
        :param raw_slug:
        :return:
        """
        result = re.sub(setting.RE_SYMBOL, ' ', raw_slug)
        hyphens_join = '-'.join(
            [item.strip().lower() if not item.strip().islower() else item.strip() for item in result.split()])
        return hyphens_join

    def resolve_conflict_slug(self, origin_slug):
        """
        生成新的 slug,通过给slug后面拼接递加数字字符实现
        :param origin_slug:
        :return:
        """
        count = 0
        while True:
            count = count + 1
            slug_title = '-'.join([origin_slug, str(count)])
            post = self.has_duplicate_slug(slug_title)
            if not post:
                return slug_title

    @staticmethod
    def has_duplicate_slug(slug_title):
        """
        判断没有重复的
        有:返回obj，没有:返回None
        :return:
        """
        post_obj = Article.query.filter(Article.slug == slug_title).one_or_none()
        return post_obj

    def new_post_action(self, author_id, category_id, all_tags_for_new_post, title, raw_slug, body_id, weight=0):
        """
        添加博文
        :param author_id: int,
        :param category_id: int,
        :param all_tags_for_new_post: list
        :param title: str,
        :param raw_slug: str,
        :param body_id: int
        :param weight:
        :return: post对象
        """
        new_identifier = self.gen_post_identifier()
        processed_slug = self.make_up_slug(raw_slug)
        try:
            assert not self.has_duplicate_slug(processed_slug)
        except AssertionError:
            processed_slug = self.resolve_conflict_slug(processed_slug)
        print(processed_slug, '------------------------')
        post = Article(title=title, slug=processed_slug, identifier=new_identifier, author_id=author_id,
                       body_id=body_id,
                       view_counts=setting.INITIAL_VIEW_COUNTS,
                       weight=weight, category_id=category_id)
        need_add_tags = assert_new_tag_in_tags(all_tags_for_new_post)
        # 正常函数不应该走到这里，因为前面已经添加了用户自主添加的，此处主要是刚开始写的代码不完善
        if need_add_tags:
            tag_poster.new_multi_tags(need_add_tags)
        for tag_name in all_tags_for_new_post:
            tag_obj = Tag.query.filter_by(tag_name=tag_name).one()
            post.tags.append(tag_obj)

        db.session.add(post)
        db.session.commit()
        # post_id = post.post_id
        return post

    def new_post(self, author_id, category_name, summary, content_html, content, title, slug, weight=0,
                 post_tags=None):
        """
        POST 博文，需要先看是否要 POST category、tag；然后 POST body；最后操作 Article 表
        :param author_id:int,
        :param category_name:str,
        :param summary:str,
        :param content_html:str,
        :param content:str,
        :param title:str,
        :param slug:str,
        :param weight:int, 1/0 表示是否置顶
        :param post_tags:list,
        :return:int,new_post_id
        """
        all_tags_for_new_post = None
        category_id = None

        if category_name:  # 新增条目？ new : get id
            category_id = category_poster.new_or_query_category(category_name)

        if post_tags:
            all_tags_for_new_post = tag_poster.add_tag_for_post(post_tags)

        body_id = self.new_post_body(summary, content_html, content)

        new_post = self.new_post_action(author_id, category_id, all_tags_for_new_post, title, slug, body_id,
                                        weight=weight)

        return new_post


class PutPostCtrl:
    """
    更新文章:更新一篇文章，要先更新标签、body表、然后再更新article
    """

    @staticmethod
    def update_post_action(post_id, all_tags_for_new_post, title, current_user_id, update_body_id, category_id,
                           weight=0):
        """
        更新文章数据的操作：先对tag进行区分，有新加的则更新；后更新文章内容
        :param post_id: str,
        :param all_tags_for_new_post: list,
        :param title: str,
        :param current_user_id: str,
        :param update_body_id: str,
        :param category_id: str,
        :param weight: int
        :return: 更新操作的文章id
        """
        need_add_tags = None
        post_obj = Article.query.filter(Article.post_id == post_id).one()
        if all_tags_for_new_post:
            need_add_tags = assert_new_tag_in_tags(all_tags_for_new_post)
            # for tag_name in all_tags_for_new_post:
            #     tag_obj = Tag.query.filter_by(tag_name=tag_name).one()
            #     post_obj.tags.append(tag_obj)
        if need_add_tags:
            tag_poster.new_multi_tags(need_add_tags)
        post_obj.title = title
        post_obj.author_id = current_user_id
        post_obj.body_id = update_body_id
        post_obj.view_counts = post_obj.view_counts
        post_obj.weight = weight
        post_obj.category_id = category_id
        post_obj.create_date = post_obj.create_date
        db.session.add(post_obj)
        db.session.commit()
        return post_obj

    @staticmethod
    def update_body(body_id, content_html, content, summary):
        """
        更新文章body
        :param body_id: str,
        :param content_html: str,
        :param content: str,
        :param summary:str,
        :return: str/None
        """
        body = ArticleBody.query.get(body_id)
        if body:
            body.content_html = content_html
            body.content = content
            body.summary = summary
            db.session.add(body)
            db.session.commit()
            return body_id
        return None

    @staticmethod
    def update_tag_for_post(post_id, post_tags=None):
        """
        更新指定文章的标签
        '''
        >>> old = {1,2,3}
        >>> now = {2,3,4,5,6}
        >>> old - now     # 原有被删的
        set([1])
        >>> now - old    #  新加的
        set([4, 5, 6])
        '''
        :return:
        """
        new_add_tags = None
        post_obj = Article.query.get(post_id)
        old_tags = {tag.tag_name for tag in post_obj.tags}
        need_del_tags = old_tags - set(post_tags)
        need_add_tags = set(post_tags) - old_tags
        if need_add_tags:  # 用户手动新增的
            new_add_tags = tag_poster.new_multi_tags(need_add_tags)
            for tag_name in need_add_tags:  # 给文章新加指定标签
                tag_obj = Tag.query.filter_by(tag_name=tag_name).one()
                post_obj.tags.append(tag_obj)

        if need_del_tags:  # 删除用户移除的标签
            for tag in need_del_tags:
                tag_obj = Tag.query.filter_by(tag_name=tag).one()
                post_obj.tags.remove(tag_obj)
                db.session.commit()
        return new_add_tags

    def update_post(self, post_id, current_user_id, category_name, summary, content_html, content, title, weight=0,
                    post_tags=None):
        """
        更新更新文章分类、标签、body
        :return:
        """
        category_id, update_body_id, all_tags_for_new_post = (None,) * 3
        if category_name:  # 新增条目？ new : get id
            category_id = category_poster.new_or_query_category(category_name)

        add_tags_for_the_post = self.update_tag_for_post(post_id, post_tags)
        post_obj = Article.query.get(post_id)
        if post_obj:
            body_id = post_obj.body_id
            update_body_id = self.update_body(body_id, content_html, content, summary)
            assert update_body_id == body_id
        update_post_obj = self.update_post_action(post_id, post_tags, title, current_user_id, update_body_id,
                                                  category_id,
                                                  weight=weight)

        return update_post_obj


class PatchPostCtrl:
    """
    关于文章的部分更新，应该在这个中进行
    """

    @staticmethod
    def add_view_count(post_id):
        """
        TODO:高级实现可以使用 redis HyperLogLog,参考:https://yemengying.com/2017/06/04/reddit-view-counting/
        https://stackoverflow.com/questions/42680357/increment-counter-for-every-access-to-a-flask-view
        https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Value
        :param post_id:
        :return:
        """
        post_obj = Article.query.filter(Article.post_id == post_id).one()
        if post_obj:
            count = post_obj.view_counts
            # https://www.jianshu.com/p/04c1ac8d9a94
            counter = Value('i', count)
            with counter.get_lock():
                counter.value += 1
            post_obj.view_counts = counter.value
            db.session.commit()
            return counter.value


class DelPostCtrl:
    """
    删除文章操作
    """

    @staticmethod
    def delete_body(body_id):
        body = ArticleBody.query.get(body_id)
        db.session.delete(body)
        db.session.commit()
        return 0

    def delete_post(self, post_id):
        """
        首先删除文章 body，然后删除文章
        :param post_id:int,
        :return:
        """
        post_obj = Article.query.filter(Article.post_id == post_id).one()
        if post_obj:
            body_id = post_obj.body_id
            for tag in post_obj.tags:
                post_obj.tags.remove(tag)
                db.session.commit()
            db.session.delete(post_obj)
            db.session.commit()
            self.delete_body(body_id)
            return post_id
