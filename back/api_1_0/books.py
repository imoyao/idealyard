#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/4 15:11

from flask import jsonify, request
from flask_restful import Resource

from back.controller import posts

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


class Books(Resource):
    BOOKS = [
        {
            'title': 'On the Road',
            'author': 'Jack Kerouac',
            'read': True
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J. K. Rowling',
            'read': False
        },
        {
            'title': 'Green Eggs and Ham',
            'author': 'Dr. Seuss',
            'read': True
        }
    ]

    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self, book_id=None):
        if book_id:
            self.response_obj['data'] = self.BOOKS[0]  # TODO: just for test
        else:
            self.response_obj['data'] = self.BOOKS
        return jsonify(self.response_obj)

    def post(self):
        post_data = request.get_json()
        print(post_data)
        self.BOOKS.append({  # TODO: 此处为自写逻辑
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
        })
        self.response_obj['msg'] = 'Books added!'
        return self.response_obj, 201

    def put(self, book_id):
        put_data = request.get_json()
        data = put_data['data']
        if book_id and self.BOOKS[0]:  # just for test
            self.BOOKS[0] = data
        return jsonify(put_data)

    def delete(self, book_id):
        if book_id:
            self.BOOKS.pop(0)
        return jsonify(self.response_obj)


class Test(Resource):
    """
    用于快速测试的一个借口
    """
    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def get(self):
        p = posts.PostNewArticle()
        self.response_obj['data'] = p.gen_post_identifier()
        return jsonify(self.response_obj)
