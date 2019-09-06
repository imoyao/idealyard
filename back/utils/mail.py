#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/31 19:06

from flask_mail import Mail, Message

mail = Mail()


class MailSender:
    """
    发送邮件
    """
    @staticmethod
    def send_mail(subject, to, body):
        with mail.connect() as conn:
            message = Message(subject, recipients=[to], body=body)
            conn.send(message)
        return 0
