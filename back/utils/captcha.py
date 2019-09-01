#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/31 0:50
"""用于生成随机验证码"""
import string
import random


class CaptchaCreator:

    @staticmethod
    def random_seq(choice_seq, count=6, repeatable=True):
        """
        生成随机数列表
        :param choice_seq:list,
        :param count: int,随机数长度
        :param repeatable: bool,是否可重复
        :return: list
        """
        if repeatable:
            return [random.choice(choice_seq) for _ in range(count)]
        return random.sample(choice_seq, count)

    def shuffle(self):
        digits = self.random_seq(string.digits)
        random.shuffle(digits)
        return ''.join(digits)


if __name__ == '__main__':
    c = CaptchaCreator()
    print(c.shuffle())
