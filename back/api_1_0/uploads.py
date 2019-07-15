#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/15 9:59
import os

from flask import request, jsonify, current_app
from flask_uploads import UploadSet, IMAGES, UploadNotAllowed
from flask_restful import Resource

from .utils import jsonify_with_args

image_upload = UploadSet('images', IMAGES)


class UploadImage(Resource):
    def __init__(self):
        self.response_obj = {'success': True, 'code': 0, 'data': None, 'msg': ''}

    def post(self):
        image_data = request.files.get('image')
        if image_data:
            base_filename = image_data.filename
            full_name = os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], base_filename)
            filename = image_upload.resolve_conflict(current_app.config['UPLOADED_IMAGES_DEST'],
                                                     base_filename) if os.path.exists(full_name) else base_filename
            # 保存上传文件
            try:
                image_obj = image_upload.save(image_data, name=filename)
            except UploadNotAllowed as e:
                self.response_obj['code'] = 1
                self.response_obj['success'] = False
                return jsonify_with_args(self.response_obj, 415)
            # 获取上传图片的URL
            img_url = image_upload.url(image_obj)
            data = {'url': img_url}
            self.response_obj['data'] = data
            return jsonify(self.response_obj)

        else:
            self.response_obj['code'] = 1
            self.response_obj['success'] = False
            return jsonify_with_args(self.response_obj, 400)
