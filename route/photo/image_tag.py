#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-08-31 0:21
import os, sys, re, json, traceback, time, datetime, pymysql
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
from tools.utils.simple_utils import file_extension, get_uuid
from conf.conf import MYSQL_DATABASE, MYSQL_PORT, MYSQL_ADDRESS, MYSQL_PASSWORD, MYSQL_USERNAME


class ImageTag(object):
    def __init__(self, id=None, image_id=None, tag_id=None):
        if id:
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "SELECT a.id,b.file_name,c.tag_name FROM `image_tag` a " \
                  "LEFT JOIN `image` b ON a.image_id=b.id " \
                  "LEFT JOIN `tag` c ON a.tag_id=c.id " \
                  "WHERE a.id=%s;"
            field_values = (id)
            cursor.execute(sql, field_values)
            result = cursor.fetchone()
            conn.close()
            self.id = result[0]
            self.file_name = result[1]
            self.tag_name = result[2]
            self.create_time = result[3]
        else:
            self.id = get_uuid()
            self.image_id = image_id
            self.tag_id = tag_id
            self.create_time = datetime.datetime.now()
            conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                   database=MYSQL_DATABASE, charset="utf8")
            cursor = conn.cursor()

            sql = "INSERT INTO `image_tag` VALUES (%s, %s, %s, %s);"

            field_values = (self.id, self.image_id, self.tag_id, self.create_time)
            result = cursor.execute(sql, field_values)
            conn.commit()
            conn.close()

    def search(self, tag_name=None):
        """
        根据tag_name模糊匹配
        :param tag_name:
        :return:
        """
        pass


    def delete(self):
        conn = pymysql.connect(host=MYSQL_ADDRESS, port=MYSQL_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                               database=MYSQL_DATABASE, charset="utf8")
        cursor = conn.cursor()
        sql = "DELETE FROM image_tag where id=%s;"
        result = cursor.execute(sql)
        conn.commit()
        conn.close()

    def __str__(self):
        image = dict(id=self.id, tag_name=self.tag_name, status=self.status, create_time=str(self.create_time),
                     update_time=str(self.update_time))
        return json.dumps(image)




if __name__ == "__main__":
    tag1 = Tag(tag_name="人像")
    tag2 = Tag(id=tag1.id)
    print(tag2)
    tag2.delete()
    tag3 = Tag(id=tag1.id)
    print(tag3)
