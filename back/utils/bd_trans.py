#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/7/16 10:07
"""
参见：http://api.fanyi.baidu.com/api/trans/product/apidoc
通用翻译API技术文档
"""
import os
import re
import random
import http.client
from urllib import request
from back.utils import md5_encrypt, flask_logger


class BaiduTrans:
    appid = os.getenv('BD_APP_ID')  # 你的appid
    secretKey = os.getenv('BD_SECRET_KEY')  # 你的密钥

    http_client = None
    api_url = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    def __init__(self, q_key, from_lang='auto', to_lang='en'):
        """
        初始化参数
        :param q_key: str, 查询关键字；
        :param from_lang: 翻译源语种；
        :param to_lang: 翻译目的语种；
        """
        self.q = q_key
        self.from_lang = from_lang
        self.to_lang = to_lang

    def re_zh_hans_from_src(self, src_lang=''):
        """
        TODO: 对于中英文混杂的字符串，需要对中文提取翻译之后返回原句
        提取中文字符
        :return:
        """
        from_string = self.from_lang if not src_lang else src_lang
        ste = re.sub(r'[A-Za-z0-9\!\%\[\]\,\。]', "", from_string)
        return ste

    def sign(self):
        """
        签名生成方法如下：

        1、将请求参数中的 APPID(appid), 翻译query(q, 注意为UTF-8编码), 随机数(salt), 以及平台分配的密钥(可在管理控制台查看)

        按照 appid+q+salt+密钥 的顺序拼接得到字符串1。

        2、对字符串1做md5，得到32位小写的sign。
        :return:
        """
        join_sign = None
        try:
            logger = flask_logger.register_logger(__name__)
            logger.info(f'{[self.appid, self.q, str(self.salt), self.secretKey]}')
            join_sign = ''.join([self.appid, self.q, str(self.salt), self.secretKey])
        except TypeError:
            print('Check you env for baidu translate API.')
        logger = flask_logger.register_logger(__name__)
        logger.info(f'{join_sign}')
        assert join_sign
        _sign = md5_encrypt(join_sign)
        return _sign

    def trans_url(self, from_lang='auto', to_lang='en'):
        """
        组装翻译url
        :param from_lang: str, http://api.fanyi.baidu.com/api/trans/product/apidoc#languageList
        :param to_lang:
        :return:str,
        """
        sign = self.sign()
        _trans_url = ''.join([self.api_url, '?appid=', self.appid, '&q=', request.quote(
            self.q), '&from=', from_lang, '&to=', to_lang, '&salt=', str(
            self.salt), '&sign=', sign])
        return _trans_url

    def trans_response(self):
        """
        请求返回结果
        :return:
        """
        _trans_url = self.trans_url()
        http_client = None
        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', _trans_url)
            # response是HTTPResponse对象
            response = http_client.getresponse()
            return response.read()
        except Exception as e:
            print(e)
        finally:
            if http_client:
                http_client.close()


def main(q_key, from_lan='auto', to_lan='en'):
    bd_trans = BaiduTrans(q_key, from_lan, to_lan)
    _ret = bd_trans.trans_response()
    return _ret


if __name__ == '__main__':
    _q_key = input('Please enter what your wanna to translate:')
    ret = main(_q_key)
    print(ret)
