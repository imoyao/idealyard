#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/8/31 19:06
import os
import time

from flask_mail import Mail, Message
from back import setting
from back.utils import flask_logger

mail = Mail()


class MailSender:
    """
    发送邮件
    """

    @staticmethod
    def makeup_send_reset_pw_mail(req_ip, captcha):
        """

        :param req_ip:
        :param captcha:
        :return:
        """
        email_data = dict()
        _subject = '重设别院牧志帐号密码'
        _body = f'''
    已收到你的密码重设要求，请输入验证码：{captcha}，该验证码 {setting.TEMPORARY_PW_EXPIRE_MINUTES} 分钟内有效。
    本次请求者IP为：{req_ip} ，若非您本人操作，请及时修改登录密码，以保证账户安全。 

    感谢对 别院牧志 的支持，再次希望你在 别院牧志 的体验有益和愉快。

    -- 别院牧志

    (这是一封自动产生的 email ，请勿回复。)
    '''
        email_data['subject'] = _subject
        email_data['body'] = _body
        return email_data

    @staticmethod
    def makeup_send_backup_data_mail(back_up_files):
        """
        # TODO:加密发送，用户解压必须去登录后台请求密码
        :param back_up_files:
        :return:
        """
        assert len(back_up_files) == 2
        new_name, old_name = back_up_files
        now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        email_data = dict()
        _subject = '博客数据备份'
        _body = f'''
        人生没有彩排，但数据必须备份。本次备份数据信息如下：

        备份时间：{now_time};
        备份文件：{new_name};
        回滚文件：{old_name};

        请下载并做好数据备份工作，以备不时之需。

        -- 别院牧志

        (这是一封自动产生的 email ，请勿回复。)
        '''
        email_data['subject'] = _subject
        email_data['body'] = _body
        return email_data

    @staticmethod
    def send_mail(subject, to, body, annex_fp_lists=None):
        """
        发送邮件
        update:2019-09-13 12:16:27：可发送带附件邮件
        :param subject:
        :param to:
        :param body:
        :param annex_fp_lists:
        :return:int,0
        """
        logger = flask_logger.register_logger(__name__)
        logger.info(f'11111111111===========111111111 ==================11111111111.')
        logger.info(f'11111111111==={subject}, {to},{body}============11111111111.')
        message = Message(subject, recipients=[to], body=body)
        logger.info(f'0000000000===========2222222222222==================0000000000.')
        # msg.attach("文件名", "类型", 读取文件）
        if annex_fp_lists:
            for annex_fp in annex_fp_lists:
                if annex_fp and os.path.exists(annex_fp) and os.path.isfile(annex_fp):
                    _, annex_name = os.path.split(annex_fp)
                    with open(annex_fp) as fp:
                        message.attach(annex_name, "application/octet-stream", fp.read())
        logger.info(f'1111==========={message} ==================1111.')
        mail.send(message)
        return 0
