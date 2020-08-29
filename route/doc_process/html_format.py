#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/5/17 下午3:42
import os, sys, re, json, traceback
from flask_restful import Resource
from flask import Flask, request, send_file, render_template, send_from_directory
from tools.utils import simple_utils as utils
from tools.html_parser.my_parser import MyParser




class HtmlFormat(Resource):
    def get(self):
        return render_template("html_parser/upload_file.html")
    def post(self):
        # 获取数据
        file = request.files['file']
        file_name = file.filename
        # 判断文件类型
        if utils.file_extension(file.filename) not in [".html", ".jhtml"]:
            return "文件格式错误，请上传html"
        # 需要保存的路径
        file_uuid = utils.get_uuid()
        print(file_uuid)
        upload_path = os.path.join('files', file_uuid + utils.file_extension(file_name))
        # 进行文件保存
        file.save(upload_path)
        # 进行解析
        f = open(upload_path, "r")
        html_data = f.read().replace("\n", " ").replace("\t", " ").replace("!DOCTYPE ", "")
        f.close()
        my_parser = MyParser()
        my_parser.feed(html_data)
        my_parser.merge_body()
        # my_parser.body.children[0].print_node(0)
        zTree_json = dict()
        my_parser.body.children[0].get_zTree_json(zTree_json=zTree_json)
        # my_parser.body.find_html_by_location(start_location="html[1]-body[2]-div[2]-div[2]-div[1]-div[1]-div[1]-div[1]-div[1]-h2[1]" ,end_location="html[1]-body[2]-div[2]-div[2]-div[1]-div[1]-div[1]-div[1]-div[3]")
        # print(json.dumps(zTree_json, ensure_ascii=False, indent=2))
        print(zTree_json)
        return render_template("html_parser/show_structure.html", html_show=my_parser.body.children[0].get_node_print(),
                               structure=zTree_json)
        # return my_parser.body.children[0].get_structure_html()




if __name__ == "__main__":
    pass
