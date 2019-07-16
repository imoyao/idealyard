#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 15:23

from back.controller import MakeupPost
from back.models import Tag, db
from back.utils.date import DateTime

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
            tag['tagname'] = tag_name
            tag['articles'] = articles
            tag['article_counts'] = data_obj.articles.count()
            all_tags[tag_name] = tag
        return all_tags

    # def show_all_tags(self, limit_count=0):
    #     """
    #     查询所有的tag 信息 （全查）
    #     :param hot:热度排序
    #     :param limit_count:int,限制数量
    #     :return:
    #     """
    #     tag_data = self.query_all_tags()
    #     limit_data = MakeupPost.make_data_limit(tag_data, limit_count)
    #     all_tags = self._make_up_tag_with_post_info(limit_data)
    #     return all_tags

    def order_tags_by_include_post_counts(self, limit_count, desc=True):
        """
        按照标签热度排就是按照各标签下文章的个数排
        :param limit_count:int,限制数量
        :param desc:bool
        :return:
        """
        # 如果按照热度排序，则不能在此处切割，否则数据不完整，热度无法获取
        tags_data = self.query_all_tags()
        tags_info = self._make_up_tag_with_post_info(tags_data)
        tags_sorted = self.sort_tags(tags_info, reverse=desc)
        limit_data = MakeupPost.make_data_limit(tags_sorted, limit_count)
        # 把列表展开放到字典中，因为标签是唯一的
        data = self.compress_tag_item_for_index(limit_data)
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
        if query_key:
            assert query_by in ['tag_name', 'tag_id']
            if query_by == 'tag_name':
                assert isinstance(query_key, str)
                query_data = Tag.query.filter(Tag.tag_name == query_key)
            elif query_by == 'tag_id' and query_key:
                # 按照 id 查询
                query_data = Tag.query.filter(Tag.id == query_key)
        else:
            query_data = Tag.query
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
        :param order_by_desc: bool
        :param limit_count:int,截取
        :return:
        """
        if hot:
            data = self.order_tags_by_include_post_counts(limit_count, desc=order_by_desc)
        else:
            query_data = self.query_tag_by(query_key, query_by=query_by, order_key=order_by,
                                           order_by_desc=order_by_desc)
            data = self._make_up_tag_with_post_info(query_data)

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
        new_tag = Tag.query.filter_by(tag_name=tag_name).one_or_none()
        if new_tag is None:     # 没有的话再去添加
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

    def add_tag_for_post(self, post_tags):
        """
        # 差集：need_pin_tags = user_post_tags-already_exist_tags
        # get_all_tags = tags.all_tags()
        :param post_tags:list,用户提交的文章 tag
        :return:
        """
        assert post_tags
        assert not isinstance(post_tags, str)
        # 新增 tag 没有默认id,过滤拿到之后去 POST
        new_add_tags = []
        tags_to_set = set(post_tags)
        _all_tags = GetTagCtrl.query_all_tags()
        all_exist_tags = set([tag.tag_name for tag in _all_tags])
        user_choose_exist = all_exist_tags & tags_to_set
        need_pin_tags = tags_to_set - user_choose_exist
        if need_pin_tags:
            new_add_tags = self.new_multi_tags(need_pin_tags)
        all_tags_for_new_post = set(user_choose_exist) | set(new_add_tags)
        # 验证相等
        assert not (all_tags_for_new_post - tags_to_set)
        return tags_to_set
