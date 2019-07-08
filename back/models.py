#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/24 9:37
"""
定义所有需要用到的表结构
"""
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

from back.exception import ValidationError

db = SQLAlchemy()


class User(db.Model):
    """
    用户表结构
    """
    __tablename__ = 'iy_user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    # 因为有用户名登录选项，所以此处必须唯一
    username = db.Column(db.String(64), index=True, unique=True, comment='用户名')
    name = db.Column(db.String(32), comment='真实姓名')
    password = db.Column(db.String(128), comment='密码，加密保存')
    email = db.Column(db.String(120), index=True, unique=True, comment='注册邮箱')
    location = db.Column(db.String(64), comment='居住地')
    slogan = db.Column(db.String(64), server_default='唯有文字能担当此任，宣告生命曾经在场。', comment='Slogan')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='用户创建时间')
    last_login = db.Column(db.DateTime(), default=datetime.utcnow, comment='最近登录时间')
    confirmed = db.Column(db.Boolean, default=False, comment='注册确认')
    avatar_hash = db.Column(db.String(32), comment='头像')
    articles = db.relationship('Article')

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        """
        密码加密
        :param password:原始密码
        :return:
        """
        self.password = custom_app_context.encrypt(password)
        return self.password

    def verify_user_password(self, password):
        """
        验证密码
        :param password:str,原始密码
        :return:bool
        """
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        """
        获取token，有效时间10min  >> 10*60
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        使用token方式认证，解析token，确认登录的用户身份
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        # 根据id查询，查到则认证通过，否则校验失败
        user = User.query.get(data['id'])
        return user


# Create M2M table
# 标签和文章为多对多关系，创建中间表
posts_tags_table = db.Table('iy_post_tags', db.Model.metadata,
                            db.Column('post_id', db.Integer, db.ForeignKey('iy_article.post_id')),
                            db.Column('tag_id', db.Integer, db.ForeignKey('iy_tag.id'))
                            )


class Article(db.Model):
    """
    文章表结构
    """
    __tablename__ = 'iy_article'
    __table_args__ = {'extend_existing': True}
    post_id = db.Column(db.Integer, primary_key=True, comment='主键')
    title = db.Column(db.String(64), comment='文章标题')
    identifier = db.Column(db.Integer, unique=True, comment='文章标识码')
    author_id = db.Column(db.Integer, db.ForeignKey('iy_user.id'), comment='作者id')
    body_id = db.Column(db.Integer, db.ForeignKey('iy_article_body.id'), unique=True, comment='文章结构体id')
    view_counts = db.Column(db.Integer, server_default='0', comment='文章阅读数')
    weight = db.Column(db.Integer, comment='置顶功能')
    category_id = db.Column(db.Integer, db.ForeignKey('iy_category.id'), comment='分类')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='文章创建时间')
    update_date = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                            comment='文章更新时间')
    # tags = db.relationship('Tag', secondary=posts_tags_table,
    #                        back_populates='articles')
    '''
    # https://stackoverflow.com/questions/36225736/flask-sqlalchemy-paginate-over-objects-in-a-relationship
    # http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
    # https://stackoverflow.com/questions/23469093/flask-sqlalchemy-query-in-a-many-to-many-itself-relationship
    
    backref 和 lazy 意味着什么了？backref 是一个在 Address 类上声明新属性的简单方法。您也可以使用 my_address.person 来获取使用该地址(address)的人(person)。
    lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据:
    'select' (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
    'joined' 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
    'subquery' 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
    'dynamic' 在有多条数据的时候是特别有用的。不是直接加载这些数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。
    您如何为反向引用（backrefs）定义惰性（lazy）状态？使用 backref() 函数:
    '''
    # 注意：dynamic 会每次都进行查询，对性能有影响，不到不得已，不要使用该设置
    tags = db.relationship('Tag', secondary=posts_tags_table, backref=db.backref('articles', lazy='dynamic'),
                           lazy="dynamic")

    authors = db.relationship('User',
                              back_populates='articles')
    categories = db.relationship('Category',
                                 back_populates='articles')
    comments = db.relationship('Comment', back_populates='articles', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Article %r>' % self.title

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post dose not have a body.')
        return Article(body=body)

    @staticmethod
    def update_post_by_id(post_id, post_info):
        """
        更新硬件信息
        :return:
        """
        post_obj = Article.query.filter(Article.post_id == post_id).first()
        post_obj.title = post_info['title']
        post_obj.author_id = post_info['author_id']
        post_obj.body_id = post_info['body_id']
        post_obj.view_counts = post_info['view_counts']
        post_obj.weight = post_info['weight']
        post_obj.category_id = post_info['category_id']
        post_obj.create_date = post_info['create_date']
        db.session.add(post_obj)
        db.session.commit()


class Tag(db.Model):
    """
    标签 表结构
    """
    __tablename__ = 'iy_tag'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    tag_name = db.Column(db.String(24), comment='标签名称')

    # articles = db.relationship('Article', secondary=posts_tags_table,
    #                            back_populates='tags')

    def __repr__(self):
        return '<Tag %r>' % self.tag_name

    def to_json(self):
        data = {'id': self.id,
                'tag_name': self.tag_name
                }
        return data


class ArticleBody(db.Model):
    """
    文章结构体 表结构
    """
    __tablename__ = 'iy_article_body'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    content_html = db.Column(db.Text, comment='文章的html')
    content = db.Column(db.Text, comment='文章内容')
    summary = db.Column(db.String(1000), server_default='你如今的气质里，藏着你走过的路、读过的书和爱过的人。', comment='文章摘要')

    def __repr__(self):
        return '<ArticleBody %r>' % self.id


class Category(db.Model):
    """
    分类 表结构
    """
    __tablename__ = 'iy_category'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    category_name = db.Column(db.String(32), unique=True, comment='分类名称')
    description = db.Column(db.String(255), comment='分类描述')
    articles = db.relationship('Article')

    def __repr__(self):
        return '<Category %r>' % self.category_name


class Comment(db.Model):
    """
    评论表，暂时只建表，不未开发相应功能
    """
    __tablename__ = 'iy_comment'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), comment='评论者名称')
    email = db.Column(db.String(64), comment='评论者邮箱')
    site = db.Column(db.String(64), comment='评论者网址')
    body = db.Column(db.Text, comment='评论内容')
    from_admin = db.Column(db.Boolean, default=False, comment='来自作者')
    reviewed = db.Column(db.Boolean, default=False, comment='评论审核')
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='评论时间')
    commented_post_id = db.Column(db.Integer, db.ForeignKey('iy_article.post_id'), comment='评论文章id')
    # 被回复id
    replied_id = db.Column(db.Integer, db.ForeignKey('iy_comment.id'), comment='回复id')
    articles = db.relationship('Article', back_populates='comments')
    # 被回复
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # 回复的评论
    replies = db.relationship('Comment', back_populates='replied', cascade='all,delete-orphan')


class SysLog(db.Model):
    """
    操作日志 表结构
    """
    __tablename__ = 'iy_syslog'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    op_ip = db.Column(db.String(64), comment='操作者ip')
    operator = db.Column(db.String(64), comment='操作者')
    op_module = db.Column(db.String(255), comment='操作模块')
    operation = db.Column(db.String(64), comment='操作事件')
    op_time = db.Column(db.DateTime(), default=datetime.utcnow, comment='操作时间')

    def __repr__(self):
        return '<ArticleBody %r>' % self.operation


class Friend(db.Model):
    """
    友链 表结构
    """
    __tablename__ = 'iy_friend'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    friend_name = db.Column(db.String(64), comment='好友名称')
    description = db.Column(db.String(255), comment='好友描述')
    friend_link = db.Column(db.String(64), comment='友链')

    def __repr__(self):
        return '<Friend %r>' % self.friend_name
