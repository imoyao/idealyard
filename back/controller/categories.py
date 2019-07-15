#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/6/29 22:28
from back.controller import QueryComponent
from back.models import Article, Category
from back.models import db

"""
分类 按照类别分组
"""


class GetCategoryCtrl:
    @staticmethod
    def query_all_category():
        return Category.query.all()

    @staticmethod
    def posts_for_category(category_id):
        """
        # TODO: 这个函数过滤有问题
        根据分类 id 查找文章
        :param category_id:
        :return:
        """
        category_data = QueryComponent.category_for_post(category_id)
        post_data = Article.query.filter_by(category_id=category_id).all()
        # TODO: 如果需要返回文章详情，此处扩写
        articles = [data.post_id for data in post_data]
        category_data['articles'] = articles
        category_data['article_counts'] = len(post_data)
        return category_data

    def show_categories(self):
        """
        显示所有的分类信息
        :return:
        """
        categories_data = Category.query.order_by(Category.id).all()
        all_data = []
        for category in categories_data:
            category_item = {}
            # hint:查询之后拿结果直接A.b 而不是 A[b]
            category_id = category.id
            articles = self.posts_for_category(category_id)
            category_item['id'] = category_id
            category_item['article_counts'] = articles['article_counts']
            category_item['articles'] = articles
            category_item['description'] = category.description
            category_item['categoryname'] = category.category_name
            all_data.append(category_item)
        return all_data


# POST
class PostCategoryCtrl:

    @staticmethod
    def new_or_query_category(category_name, description=''):
        """
        如果已存在，则查找id,否则新建分类
        :param category_name:
        :param description:
        :return:
        """
        assert category_name
        already_exist_category = {category.category_name: category.id for category in
                                  GetCategoryCtrl.query_all_category()}
        if already_exist_category and category_name in already_exist_category.keys():
            category_id = already_exist_category[category_name]
        else:
            category = Category(category_name=category_name, description=description)
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        return category_id
