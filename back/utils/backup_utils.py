#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2019/9/13 10:18
"""
备份数据库
每周一次
对比文件，如果文件存在则对比差异并生成html，发送带附件邮箱（上次的和本次的）
备份之后发送到个人邮箱

"""
import time
import os

from back import setting
from back.utils import flask_logger


class BackupDB:

    @staticmethod
    def back_up_file_path():
        back_up_fp = os.path.join(setting.BASE_DIR, setting.BACK_UP_DATA_FP)
        return back_up_fp

    def make_up_file_name(self, db):
        """
        备份文件名：ip_database_strftime
        :param db:
        :return:
        """
        now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        nodename = os.uname().nodename
        file_name = '_'.join([nodename, db.upper(), now_time])
        real_file_name = f'{file_name}.sql.gz'
        back_up_fp = self.back_up_file_path()
        assert os.path.exists(back_up_fp) and os.path.isdir(back_up_fp)
        fp = os.path.join(back_up_fp, real_file_name)
        return fp

    def back_up_action(self, user, pw, db, host='localhost', port=3306):
        logger = flask_logger.register_logger(__name__)
        nt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fn = self.make_up_file_name(db)
        # 格式：mysqldump -h主机名 -P端口 -u用户名 -p密码 --databases 数据库名 | gzip > 文件名.sql.gz
        back_cmd = f'mysqldump -h{host} -P{port} -u{user} -p{pw} --databases {db} | gzip > {fn}'
        logger.info(f'The backup CMD is: {back_cmd}.')
        ret_code = os.system(back_cmd)
        if ret_code == 0:
            logger.info(f'The System has backup database {db} success at {nt}.')
        else:
            logger.error(f'The System backup database {db} failed at {nt}.')
        return fn


def main():
    bker = BackupDB()
    user_name = os.getenv('MYSQL_USER', setting.DB_USER)
    password = os.getenv('MYSQL_PASSWORD', setting.DB_PASSWORD)
    file_fp = bker.back_up_action(user_name, password, setting.DATABASE_NAME)
    return file_fp


if __name__ == '__main__':
    ret = main()
    print(ret)
