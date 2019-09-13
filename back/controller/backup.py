#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/9/13 13:31
import os
from back import setting
from back.utils.mail import MailSender

from back.utils import backup_utils, flask_logger
from back.celery_components import tasks as celery_tasks

backer = backup_utils.BackupDB()
sender = MailSender()


class BackupCtrl:

    @staticmethod
    def send_back_up_mail(back_up_files, receiver):
        """
        发送邮件
        :param back_up_files:
        :param receiver:
        :return:
        """
        _email_data = sender.makeup_send_backup_data_mail(back_up_files)
        logger = flask_logger.register_logger(__name__)
        logger.info(
            f'-------------ssss :{back_up_files},{receiver} ---------------ssss.')
        sender.send_mail(_email_data['subject'], receiver, _email_data['body'], annex_fp_lists=back_up_files)
        return 0

    @staticmethod
    def rename_and_remove_back_up(back_packages):
        """
        删除上次备份文件，并把本次文件重命名成备份文件
        新生成的重命名，旧的直接删除
        :return:
        """
        back_up_fp = backer.back_up_file_path()
        assert os.path.exists(back_up_fp)
        assert len(back_packages) == 2
        new, old = back_packages
        origin_fp = os.path.join(back_up_fp, new)
        new_name_for_backup = f'{back_up_fp}{setting.BACKUP_PREFIX}{new}'
        recover_fp = os.path.join(back_up_fp, new_name_for_backup)
        os.rename(origin_fp, recover_fp)

        old_fp = os.path.join(back_up_fp, old)
        os.remove(old_fp)
        return 0

    def mail_back_up_action(self, back_recipient_mail):
        """
        导出数据库
        获取上次备份和本次备份文件名称
        发送邮件
        :param back_recipient_mail:
        :return:list,有序列表，前面是新文件，后面是旧文件
        """
        logger = flask_logger.register_logger(__name__)
        back_packages = []
        logger.info(
            f'There are redundant file========back_recipient_mail :{back_recipient_mail} and will be remove now.')
        new_file, old_file = ('',) * 2
        new_back_file_fp = backup_utils.main()
        logger.info(f'new_back_file_fp==========={new_back_file_fp} ==================new_back_file_fp.')
        if new_back_file_fp:
            back_files = []
            back_up_fp = backer.back_up_file_path()
            for root, dirs, files in os.walk(back_up_fp):
                if root == back_up_fp:
                    back_files = files
            back_file_pop_redundancy = [f for f in set(back_files) if not f.startswith('.')]
            logger.info(
                f'new_back_file_fp======111====={back_file_pop_redundancy} =======1111===========new_back_file_fp.')
            try:
                assert len(back_file_pop_redundancy) <= 2
            except AssertionError:
                files = ';'.join(back_file_pop_redundancy)
                logger.info(f'There are redundant file :{files} and will be remove now.')
                for file in back_file_pop_redundancy:  # 多于两个，则清空目录，5分钟后重新备份
                    file_fp = os.path.join(back_up_fp, file)
                    os.remove(file_fp)
                # # TODO:再次执行备份计划
                # task = celery_tasks.send_reset_password_mail_long_task.apply_async(args=(setting.SEND_BACKUP_TO_MAIL,),
                #                                                                    queue='mail',
                #                                                                    routing_key='mail', countdown=5 * 60)
                # logger.info(f'We resend backup mail to admin,you can get info by check for celery task: {task.id} .')
            for file in back_file_pop_redundancy:
                if file.startswith(setting.BACKUP_PREFIX):  # 之前备份过
                    old_file = file
                else:
                    new_file = file  # 之前没备份过
            dirname, new_back_file = os.path.split(new_back_file_fp)
            logger.info(
                f'new_back_file_fp=====333333333===={new_file == new_back_file} =======3333333==========new_back_file_fp.')
            assert new_file == new_back_file
            back_packages.append(os.path.join(back_up_fp, new_file))
            if old_file:
                back_packages.append(os.path.join(back_up_fp, old_file))
            else:
                back_packages.append(None)
            logger.info(
                f'new_back_file_fp=====4444444===={back_packages} =======44444444444444==========new_back_file_fp.')
            ret = self.send_back_up_mail(back_packages, back_recipient_mail)
            return back_packages
        else:
            return 1
