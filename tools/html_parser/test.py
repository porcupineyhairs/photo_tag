#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/4/19 下午2:45
import os, sys, re, json, traceback
from tools.utils.simple_utils import get_file_names
from tools.html_parser.my_parser import MyParser
from tools.html_parser import web_node as wn

def example1():

    my_parser = MyParser()
    my_parser.feed(open('html/5745fb65ab274da2923ecbe8cfd50546.html', 'r').read())
    data = my_parser.body
    my_parser.merge_body(data)
    my_parser.close()
    result1 = []
    data.print_mulu([u"技术部分", u"货物技术要求", u"货物技术规范书"], result1)
    result2 = []
    data.print_mulu([u'投标文件格式', u'评标办法（经评审的最低评标价法）'], result2)
    # print(data.children[0].get_node_print())
    # print(data.find_tag("text").path)
    if len(result1)>0 and len(result2)>0:
        # print "len(result1)={0}".format(len(result1))
        article_start = result1[len(result1)-1]
        print(article_start[0])
        article_start_location = article_start[3]
        article_end_location = ""
        for each in result2:
            if wn.compare_location(article_start[3], each[3], True):
                print(each[0])
                article_end_location = each[3]
                break
        if article_end_location == "":
            print("没有找到文档结束位置")
        # head = my_parser.body.find_tag(tag="head")
        # head.print_node(0)
        #
        # body = my_parser.body.find_tag(tag="body")
        # body.print_node(0)

        print(article_start_location)
        print(article_end_location)

        data.find_html_by_location(start_location=article_start_location, end_location=article_end_location)


        print(data.children[0].get_node_print())


if __name__ == "__main__":
    # html[1]-body[2]-ol[204]-li[1]-strong[1]-span[1]
    # html[1]-body[2]-p[1]-text[3]
    example1()
