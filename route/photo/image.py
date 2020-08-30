#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-08-31 0:21
import os, sys, re, json, traceback, time, datetime, pymysql
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
from tools.utils.simple_utils import file_extension, get_uuid
from conf.conf import MYSQL_DATABASE, MYSQL_PORT, MYSQL_ADDRESS, MYSQL_PASSWORD, MYSQL_USERNAME


class Image(object):
    SHOW = 0
    NOSHOW = 1

    def __init__(self, id=None, file_name=None):
        if id:
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "SELECT * FROM `image` WHERE id=%s;"
            field_values = (id)
            cursor.execute(sql, field_values)
            result = cursor.fetchone()
            conn.close()
            self.id = result[0]
            self.save_name = result[1]
            self.save_type = result[2]
            self.file_name = result[3]
            self.status = result[4]
            self.create_time = result[5]
            self.update_time = result[6]
        else:
            self.id = get_uuid()
            self.save_name = self.id
            self.save_type = file_extension(file_name)[1:]
            self.file_name = file_name[:len(file_name) - len(self.save_type) - 1]
            self.status = Image.SHOW
            self.create_time = datetime.datetime.now()
            self.update_time = datetime.datetime.now()
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "INSERT INTO `image` VALUES (%s, %s, %s, %s, %s, %s, %s);"

            field_values = (self.id, self.save_name, self.save_type, self.file_name, self.status,
                            self.create_time, self.update_time)
            result = cursor.execute(sql, field_values)
            conn.commit()
            conn.close()

    @staticmethod
    def search(start_time=None, begin_time=None, tag_id_list=None):
        """
        根据起始日期和结束日期查询   以及根据多个tag进行查询
        :param start_time:
        :param begin_time:
        :param tag_id_list:
        :return:
        """
        pass


    def delete(self):
        conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                               database=MYSQL_DATABASE, charset="utf8")
        cursor = conn.cursor()
        sql = "UPDATE image set status=%s where id=%s;"
        field_values = (Image.NOSHOW, self.id)
        result = cursor.execute(sql, field_values)
        conn.commit()
        conn.close()

    def __str__(self):
        image = dict(id=self.id, save_name=self.save_name, save_type=self.save_type, file_name=self.file_name,
                     status=self.status, create_time=str(self.create_time), update_time=str(self.update_time))
        return json.dumps(image)




if __name__ == "__main__":
    image1 = Image(file_name="test1.png")
    image2 = Image(id=image1.id)
    print(image2)
    image2.delete()
    image3 = Image(id=image1.id)
    print(image3)
