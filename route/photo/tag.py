#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-08-31 0:21
import os, sys, re, json, traceback, time, datetime, pymysql
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
from tools.utils.simple_utils import file_extension, get_uuid
from conf.conf import MYSQL_DATABASE, MYSQL_PORT, MYSQL_ADDRESS, MYSQL_PASSWORD, MYSQL_USERNAME


class Tag(object):
    SHOW = 0
    NOSHOW = 1

    def __init__(self, id=None,tag_name=None):
        if id:
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "SELECT * FROM `tag` WHERE id=%s;"
            field_values = (id)
            cursor.execute(sql, field_values)
            result = cursor.fetchone()
            conn.close()
            self.id = result[0]
            self.tag_name = result[1]
            self.status = result[2]
            self.create_time = result[3]
            self.update_time = result[4]
        else:
            self.id = get_uuid()
            self.tag_name = tag_name
            self.status = Tag.SHOW
            self.create_time = datetime.datetime.now()
            self.update_time = datetime.datetime.now()
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "INSERT INTO `tag` VALUES (%s, %s, %s, %s, %s);"

            field_values = (self.id, self.tag_name, self.status, self.create_time, self.update_time)
            result = cursor.execute(sql, field_values)
            conn.commit()
            conn.close()

    @staticmethod
    def search(tag_name=None):
        """
        根据tag_name模糊匹配
        :param tag_name:
        :return:
        """
        conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                               database=MYSQL_DATABASE, charset="utf8")
        cursor = conn.cursor()

        sql = "SELECT * FROM `tag` where status=%s;"
        field_values = (Tag.SHOW)
        cursor.execute(sql, field_values)
        result = cursor.fetchall()
        conn.close()
        result2 = list()
        for each in result:
            result2.append(dict(
                id=each[0],
                tag_name=each[1],
                status=each[2],
                create_time=each[3],
                update_time=each[4]
            ))
        return result2


    def delete(self):
        conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                               database=MYSQL_DATABASE, charset="utf8")
        cursor = conn.cursor()
        sql = "UPDATE tag set status=%s where id=%s;"
        field_values = (Tag.NOSHOW, self.id)
        result = cursor.execute(sql, field_values)
        conn.commit()
        conn.close()

    def __str__(self):
        image = dict(id=self.id, tag_name=self.tag_name, status=self.status, create_time=str(self.create_time),
                     update_time=str(self.update_time))
        return json.dumps(image)




if __name__ == "__main__":
    print(Tag.search())
    # tag1 = Tag(tag_name="tag1")
    # tag1 = Tag(tag_name="tag2")
    # tag1 = Tag(tag_name="tag3")
    # tag1 = Tag(tag_name="tag4")
    # tag1 = Tag(tag_name="tag5")
    # tag2 = Tag(id=tag1.id)
    # print(tag2)
    # tag2.delete()
    # tag3 = Tag(id=tag1.id)
    # print(tag3)
