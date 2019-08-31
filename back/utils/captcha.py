#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/31 0:50
"""用于生成随机验证码"""
import string
import random


class CaptchaCreator:

    @staticmethod
    def random_seq(choice_seq, count=6):
        return random.sample(choice_seq, count)

    def shuffle(self):
        digits = self.random_seq(string.digits)
        random.shuffle(digits)
        return ''.join(digits)


if __name__ == '__main__':
    c = CaptchaCreator()
    print(c.shuffle())
