#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/4/17 下午5:03
import os, sys, re, json, traceback


# 判定两个path前者是否在后者前面，在True，不在False。equal_boo设定是否可以相等
def compare_location(location1, location2, equal_boo):
    pat = "\[(\d+)\]"
    num_str_list1 = re.findall(pat, location1)
    num_str_list2 = re.findall(pat, location2)
    num_list1 = [int(each) for each in num_str_list1]
    num_list2 = [int(each) for each in num_str_list2]
    length = min(len(num_list1), len(num_list2))
    all_same = True
    for i in range(length):
        if all_same and num_list1[i] > num_list2[i]:
            return False
        if num_list1[i] != num_list2[i]:
            all_same = False
    if equal_boo:
        if all_same and len(num_list1) > len(num_list2):
            return False
    else:
        if all_same and len(num_list1) >= len(num_list2):
            return False
    return True


class WebNode(object):
    def __init__(self):
        self.father = None  # 父节点
        self.children = []  # 子节点
        self.attr = {}   # 属性
        self.content = ""  # 文字
        self.tag = ""  # 标签
        self.flag = ""  # 设置标记
        self.index = 0  # 层级
        self.path = ""  # 路径
        self.type = ""  # 类型

    def print_node(self, index):
        message = ""
        if self.tag in ["meta", "hr", "br"]:
            message += "<" + self.tag
            for each in self.attr:
                message += " " + each + "='" + self.attr[each] + "'"
            message += "/>"
            if len(message)>0:
                print("  " * index + message)
        else:
            if self.tag in ["text"]:
                if len(self.content) > 0:
                    print("  " * index + self.content)
            else:
                message += "<" + self.tag
                for each in self.attr:
                    message += " " + each + "='" + self.attr[each] + "'"
                message += ">"
                if len(self.children)>0:
                    if len(message) > 0:
                        print("  " * index + message)
                    for each in self.children:
                        each.print_node(index+1)
                    print("  " * index + "</" + self.tag + ">")
                else:
                    message += self.content + "</" + self.tag + ">"
                    if len(message) > 0:
                        print("  " * index + message)


    def get_node_print(self):
        node_print = ""
        message = ""
        if self.tag in ["meta", "hr", "br"]:
            message += "<" + self.tag
            for each in self.attr:
                message += " " + each + "='" + self.attr[each] + "'"
            message += "/>"
            node_print += message
        else:
            if self.tag in ["text"]:
                node_print += self.content
            else:
                message += "<" + self.tag
                for each in self.attr:
                    if self.attr[each]:
                        message += " " + each + "='" + self.attr[each] + "'"
                    else:
                        message += " " + each + " "
                message += ">"
                if len(self.children)>0:
                    node_print += message
                    for each in self.children:
                        node_print += each.get_node_print()
                    node_print += "</" + self.tag + ">"
                else:
                    message += self.content + "</" + self.tag + ">"
                    node_print += message
        return  node_print


    def find_tag(self, tag="body"):
        '''
        找到了文档body部分开始的那段
        :return:
        '''
        if self.tag == tag:
            return self
        else:
            for each in self.children:
                result = each.find_tag(tag=tag)
                if result != None:
                    return result


    def print_content_by_path(self, path = ""):
        for each_node in self.children:
            if path==each_node.path:
                return each_node.content
            elif path.startswith(each_node.path):
                return each_node.print_content_by_path(path)






    def find_html_by_location(self,start_location="html[1]-head[1]",end_location="html[1]-body[2]-ol[180]-li[4]-ol[51]-li[3]-span[154]"):
        if self.tag == "head":
            new_children = []
            for each in self.children:
                if each.tag not in ["link","script"]:
                    new_children.append(each)
            self.children = new_children
            return True
        if self.tag == "script":
            return False
        if len(self.children)==0 and self.type!="startendtag" and self.content=="" and self.tag not in ["td","tr","th"] :
            return False
        # print self.path,
        boo1 = compare_location(start_location, self.path, True)
        boo2 = compare_location(self.path, end_location, False)
        if len(self.children)>0:
            new_children = []
            for each in self.children:
                if each.find_html_by_location(start_location, end_location):
                    new_children.append(each)
            self.children = new_children
            if len(new_children)>0:
                return True
            else:
                return False
        else:
            return boo1 and boo2


    def print_structure(self):
        if len(self.children) > 0:
            print(self.path)
        else:
            print(self.path + ":" + self.content)

        for each in self.children:
            each.print_structure()


    def get_structure_print(self):
        structure = ""
        if len(self.children) > 0:
            structure += self.path + "\n"
        else:
            structure += self.path + ":" + self.content + "\n"

        for each in self.children:
            structure += each.get_structure_print()
        return structure


    def get_structure_html(self):
        structure = ""
        if len(self.children) > 0:
            structure += "<p>" + self.path + "</p>"
        else:
            structure += "<p>" + self.path + ":" + self.content + "</p>"

        for each in self.children:
            structure += each.get_structure_html()
        return structure


    def get_zTree_json(self, zTree_json = dict()):
        zTree_json["name"] = self.tag

        children = list()

        if len(self.attr) > 0:
            attr = dict()
            attr["name"] = "attr"
            attr_children = list()
            for each in self.attr:
                attr_children.append({"name":"{0}:{1}".format(each, self.attr[each])})
            attr["children"] = attr_children
            children.append(attr)

        if len(self.content) > 0:
            children.append({"name": "{0}:{1}".format("content", self.content)})

        children.append({"name": "{0}:{1}".format("index", self.index)})

        children.append({"name": "{0}:{1}".format("path", self.path)})

        if len(self.children)>0:
            node_children = list()
            for each in self.children:
                each_zTree_json = dict()
                each.get_zTree_json(zTree_json=each_zTree_json)
                node_children.append(each_zTree_json)
            children.append({"name": "children", "children": node_children})

        zTree_json["children"] = children
        # print(self.tag)
        # print(zTree_json["name"])
        # print(json.dumps(zTree_json))
        # return zTree_json










class PNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class ImgNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class StrongNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class SpanNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class HtmlNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)


class HeadNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class BodyNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class MetaNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class StyleNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class H1Node(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class H2Node(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class H3Node(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class HrNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class BrNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class OlNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class LiNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class TableNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class TrNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class TdNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class TextNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class TitleNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class ScriptNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class DivNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class FormNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class OptionNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class SelectNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class InputNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

class LinkNode(WebNode):
    def __init__(self):
        WebNode.__init__(self)

if __name__ == "__main__":
    pass
