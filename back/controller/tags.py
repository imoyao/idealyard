#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:23

from back.controller import MakeupPost
from back.models import Tag, db
from back.utils import DateTime

date_maker = DateTime()


class GetTagCtrl:

    @staticmethod
    def query_all_tags():
        return Tag.query.all()

    @staticmethod
    def sort_tags(unsorted_dict, reverse=True):
        """
        按照标签下的文章 count 排序
        :param unsorted_dict:
        :param reverse:
        :return:
        """
        return sorted(unsorted_dict.items(), key=lambda item: item[1]['article_counts'], reverse=reverse)

    @staticmethod
    def compress_tag_item_for_index(tags):
        """
        json数据压缩成一层
        :param tags:
        :return:
        """
        return [{'tagname': info[0], 'count': info[1]['article_counts'], 'id': info[1]['id']} for info in tags]

    @staticmethod
    def _make_up_tag_with_post_info(tag_data):
        all_tags = dict()
        for data_obj in tag_data:
            tag = dict()
            # 文章id
            # hint:注意此处，遍历之后可以反查文章信息
            articles = [data.post_id for data in data_obj.articles]
            tag_name = data_obj.tag_name
            tag['id'] = data_obj.id
            tag['tagname'] = data_obj.tag_name
            tag['articles'] = articles
            tag['article_counts'] = data_obj.articles.count()
            all_tags[tag_name] = tag
        return all_tags

    def show_all_tags(self, limit_count=0):
        """
        查询所有的tag 信息 （全查）
        :return:
        """
        tag_data = Tag.query.all()
        limit_data = MakeupPost.make_data_limit(tag_data, limit_count)
        all_tags = self._make_up_tag_with_post_info(limit_data)
        return all_tags

    def order_tags_by_include_post_counts(self, limit_count, desc=True):
        """
        按照标签热度排就是按照各标签下文章的个数排
        :param limit_count:
        :param desc:
        :return:
        """
        # TODO：这个里面的方法都要梳理
        tags_info = self.show_all_tags(limit_count)
        # 把列表展开放到字典中，因为标签是唯一的
        tags_sorted = self.sort_tags(tags_info, reverse=desc)
        data = self.compress_tag_item_for_index(tags_sorted)
        return data

    @staticmethod
    def query_tag_by(query_key, query_by='tag_id', order_key='id', order_by_desc=True):
        """
        条件查询
        **注意**：为了增加区分度，query_by和order_by传值要留神，前者是under_line_case(tag_name/tag_id),后者是case(name/id)
        :param query_key:
        :param query_by:
        :param order_key:
        :param order_by_desc:
        :return:
        """
        data = None
        query_data = None
        assert query_by in ['tag_name', 'tag_id']
        if query_by == 'tag_name':
            assert isinstance(query_key, str)
            query_data = Tag.query.filter(Tag.tag_name == query_key)
        elif query_by == 'tag_id':
            # 按照 id 查询
            query_data = Tag.query.filter(Tag.id == query_key)
        if query_data:
            assert order_key in ['id', 'name']
            if order_key == 'id':
                data = query_data.order_by(Tag.id.desc()) if order_by_desc else query_data.order_by(Tag.id)
            elif order_key == 'name':
                data = query_data.order_by(Tag.tag_name.desc()) if order_by_desc else query_data.order_by(Tag.tag_name)
        return data

    def get_tag_detail_by_args(self, query_key, query_by='tag_id', order_by='id', hot=False, order_by_desc=True,
                               limit_count=0):
        """


        根据各种条件查询标签
        :param query_key: str/int,具体的name或者id
        :param query_by: str,查询字段:tag_id <default> ,tag_name(查单个)
        :param order_by: 排序字段：id, post_count(热度),
        :param hot: bool, 是否按照热度排序
        :param order_by_desc: str, 'desc' / 'asc'
        :param limit_count:int,截取
        :return:
        """
        # https://stackoverflow.com/questions/33512126/how-to-sort-an-array-of-objects-by-datetime-in-python/33512197
        data = None
        if query_by:
            query_data = self.query_tag_by(query_key, query_by=query_by, order_key=order_by,
                                           order_by_desc=order_by_desc)
            data = self._make_up_tag_with_post_info(query_data)
        elif hot:
            data = self.order_tags_by_include_post_counts(limit_count, desc=order_by_desc)

        return data


class PostTagCtrl:

    @staticmethod
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

    def new_multi_tags(self, tag_names):
        """
        添加多个标签
        :param tag_names:list/set,
        :return:list, [tag_name1,tags_name2,……]
        """
        assert not isinstance(tag_names, str)
        assert len(tag_names) >= 1
        tags = []
        for tag_item in tag_names:
            tags.append(self.new_tag(tag_item))
        return tags

    def add_tag(self, post_tags):
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
                new_add_tags = self.new_multi_tags(new_tags)
            all_tags_for_new_post = set(origin_tags) | set(new_add_tags)
            return all_tags_for_new_post

    def add_tag_for_post(self, post_tags):
        assert post_tags
        assert not isinstance(post_tags, str)
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
            new_add_tags = self.new_multi_tags(new_tags)
        all_tags_for_new_post = set(origin_tags) | set(new_add_tags)
        return all_tags_for_new_post
