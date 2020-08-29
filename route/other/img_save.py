#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/9/10 下午2:56
import os, sys, re, json, traceback, time
from flask_restful import Resource
from flask import Flask, request, send_file, render_template, send_from_directory
from tools.utils.simple_utils import get_uuid,TreeNode

class ImgAdd(Resource):
    # 进入图片新增页面
    def get(self):
        conf_file = open("conf/img_server/show.json", "r")
        tree_info = json.loads(conf_file.read())
        conf_file.close()
        return render_template("idps/index.html", tree_info = tree_info)
    # 进行图片新增
    def post(self):
        pass

def floder_show(floder_path):
    top_floder_level = len(floder_path.split("/"))
    tree_node = None
    now_node = None
    for root, dirs, files in os.walk(floder_path):
        floder_level = len(root.split("/"))
        # print(root)
        if floder_level == top_floder_level:
            # 初始化节点
            tree_node = TreeNode(root.split("/")[floder_level - 1])
            tree_node.path = "/{0}".format(tree_node.name)
            now_node = tree_node
        elif floder_level - top_floder_level == now_node.level:
            # 同级节点
            new_node = TreeNode(root.split("/")[floder_level - 1])
            new_node.path = "{0}/{1}".format(now_node.parent.path, new_node.name)
            new_node.level = now_node.level
            new_node.parent = now_node.parent
            now_node.parent.children.append(new_node)
            now_node = new_node
        elif floder_level - top_floder_level == now_node.level + 1:
            # 子节点
            new_node = TreeNode(root.split("/")[floder_level - 1])
            new_node.path = "{0}/{1}".format(now_node.path, new_node.name)
            new_node.level = now_node.level + 1
            new_node.parent = now_node
            now_node.children.append(new_node)
            now_node = new_node
        elif floder_level - top_floder_level <= now_node.level - 1:
            for i in range(now_node.level - floder_level + top_floder_level):
                now_node = now_node.parent
            # 父节点的兄弟节点
            new_node = TreeNode(root.split("/")[floder_level - 1])

            new_node.path = "{0}/{1}".format(now_node.parent.path, new_node.name)
            new_node.level = now_node.level
            new_node.parent = now_node.parent
            now_node.parent.children.append(new_node)
            now_node = new_node
        now_node.files = files
    return tree_node

def print_node(node,index=0):
    print("{0}{1}".format("  "*index,node.name))
    if len(node.children) != 0:
        for each in node.children:
            if each != None:
                print_node(each, index+1)
        for each in node.files:
            print("{0}{1}".format("  " * (index + 1), each))

def create_tree_json(node,result = [],last_uuid = 0):
    uuid = get_uuid()
    result.append({
        "id": uuid,
        "pId": last_uuid,
        "name": node.name,
        # "url": "/static/{0}".format(node.path),
        "target": "show_iframe"
    })
    if len(node.children) != 0:
        for each in node.children:
            if each != None:
                create_tree_json(each, result=result, last_uuid=uuid)
        for each in node.files:
            result.append({
                "id": get_uuid(),
                "pId": uuid,
                "name": each,
                "url": "/static{0}/{1}".format(node.path,each),
                "target": "show_iframe"
            })


class ImgShow(Resource):
    def get(self):
        conf_file = open("conf/img_server/show.json", "r")
        tree_info = json.loads(conf_file.read())
        conf_file.close()
        tree_info.insert(0, {
            "id": "a154c40c47034c608830e3700a31548e",
            "pId": "3f9299bb8a45410d8c4adad581666fdb",
            "url": "/img_server/manage1",
            "name": "图片管理",
            "target": "show_iframe"
        })
        tree_info.insert(0, {
            "id": "0fa27afca25648f4b67c10255e257b21",
            "pId": "3f9299bb8a45410d8c4adad581666fdb",
            "url": "/img_server/manage2",
            "name": "路径管理",
            "target": "show_iframe"
        })
        tree_info.insert(0,{
            "id": "3f9299bb8a45410d8c4adad581666fdb",
            "pId": 0,
            "name": "img_manage",
            "target": "show_iframe"
        })
        return render_template("other/index.html", tree_info=tree_info)




if __name__ == "__main__":
    a = floder_show("/Users/jingjian/datagrand/gitlab/MyTools/template/img_server")
    # print_node(a)
    result = []
    create_tree_json(a, result=result)
    print(json.dumps(result, indent=2, ensure_ascii=False))

