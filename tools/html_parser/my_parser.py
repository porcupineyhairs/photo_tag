#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/4/17 下午5:03
import os, sys, re, json, traceback
from tools.html_parser import web_node as wn
from html.parser import HTMLParser


startendtag_list = ["meta", "br", "hr", "img"]
maybenoendtag_list = ["input", "link"]


class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # 放置解析之后的html主体
        self.body = wn.WebNode()
        # 解析过程中用于放置递归当前的节点
        self.now = self.body


    def handle_starttag(self, tag, attrs):
        '''
        获取起始标签 <xxx> 其中也会包括直接闭合标签例如meta,hr,br
        :param tag:标签名
        :param attrs:属性列表
        :return:
        '''

        # 父方法获取对应的标签和属性
        HTMLParser.handle_starttag(self, tag, attrs)
        # print("tag_start:{0}".format(tag))
        # 排除掉直接闭合标签的干扰
        if tag in startendtag_list:
            return

        # 新建该节点 并分辨该节点的类型
        node = wn.WebNode()
        if tag == "p":
            node = wn.PNode()
        elif tag == "strong":
            node = wn.StrongNode()
        elif tag == "span":
            node = wn.SpanNode()
        elif tag == "html":
            node = wn.HtmlNode()
        elif tag == "head":
            node = wn.HeadNode()
        elif tag == "body":
            node = wn.BodyNode()
        elif tag == "style":
            node = wn.StyleNode()
        elif tag == "h1":
            node = wn.H2Node()
        elif tag == "h2":
            node = wn.H2Node()
        elif tag == "h3":
            node = wn.H2Node()
        elif tag == "table":
            node = wn.TableNode()
        elif tag == "tr":
            node = wn.TrNode()
        elif tag == "td":
            node = wn.TdNode()
        elif tag == "ol":
            node = wn.OlNode()
        elif tag == "li":
            node = wn.LiNode()
        elif tag == "title":
            node = wn.TitleNode()
        elif tag == "div":
            node = wn.DivNode()
        elif tag == "form":
            node = wn.FormNode()
        elif tag == "select":
            node = wn.SelectNode()
        elif tag == "option":
            node = wn.OptionNode()
        elif tag == "script":
            node = wn.ScriptNode()
        elif tag == "input":
            node = wn.InputNode()
        elif tag == "link":
            node = wn.LinkNode()
        # 赋值标签，之前的当前节点赋值新节点的父节点
        node.tag = tag
        node.father = self.now
        # 判断父节点是否为空，即是否是顶层的
        if node.father != None:
            # 表明该节点比其父节点低一层
            node.index = node.father.index + 1
            # 判断父节点的path是否为空，即是否第一次记录path
            if node.father.path == "":
                # 为空则记录初始父节点
                node.path = "{0}[{1}]".format(tag, len(node.father.children)+1)
            else:
                # 不为空则继续增加路径
                node.path = node.father.path + "-" + "{0}[{1}]".format(tag, len(node.father.children)+1)
        else:
            # 没有父节点，表明其层级最高
            node.index = 0
        # 添加属性
        for each in attrs:
            node.attr[each[0]]=each[1]

        # 将新节点置为父节点，向下移一层
        self.now = node
        # 如果是可能非闭合标签 其不可能有子节点，则必然将其闭合，然后重新走start流程
        if self.now.tag in maybenoendtag_list:
            self.now.father.children.append(self.now)
            self.now = self.now.father
        # print("当前now.tag={0}".format(self.now.tag))


    def handle_endtag(self, tag):
        '''
        获取结束标签 </xxx> 其中也会包括直接闭合标签例如meta,hr,br
        :param tag:标签名
        :return:
        '''


        # 父方法获取对应的标签
        HTMLParser.handle_endtag(self, tag)
        # 排除掉直接闭合标签的干扰
        if tag in startendtag_list:
            return
        # print("tag_end:{0}".format(tag))
        # print("now.tag:{0}".format(self.now.tag))
        # print("now.path:{0}".format(self.now.path))
        # print("now.tag==tag:{0}".format(self.now.tag == tag))
        # print("now:{0}".format(self.now), end="\n\n")
        if not self.now.tag == tag:
            return
        # 标签到了闭合的地方，其必然是有父标签的，将当前节点加入父标签的子节点列表中
        self.now.father.children.append(self.now)
        # 这里还需要对当前now节点，如果其children只有一个并且是TextNode对象，则不再需要这个子节点
        children = self.now.children
        if len(children) == 1 and isinstance(children[0], wn.TextNode):
            self.now.content = children[0].content
            self.now.children = []
        # 将当前节点赋值为父节点，向上移一层
        self.now = self.now.father

        return


    def handle_data(self, data):
        '''
        获取标签中的文本信息
        :param data:文本信息
        :return:
        '''
        if len(data.replace(" ", "").replace("\n", "")) > 0:
            # print("tag_data:{0},len:{1}".format(data, len(data)))

            # 父方法获取对应的文本
            HTMLParser.handle_data(self, data)

            # 新建文本节点
            node = wn.TextNode()
            # 为其赋值标签和父节点等信息
            node.tag = "text"
            node.father = self.now
            node.content = data
            node.index = node.father.index + 1
            node.path = node.father.path + "-" + "{0}[{1}]".format("text", len(node.father.children) + 1)
            # 设定其特别的类型
            node.type = "text"
            # 将其加入父节点的子节点列表中
            self.now.children.append(node)
            # 保留其父节点完整的content属性
            self.now.content += data


    def handle_startendtag(self, tag, attrs):
        '''
        处理类似于<br/>这样的直接闭合的标签
        :param tag:
        :param attrs:
        :return:
        '''
        # print("tag_startend:{0}".format(tag))
        # 父方法获取对应的标签和属性
        HTMLParser.handle_startendtag(self, tag, attrs)
        # 新建该节点 并分类
        node = wn.WebNode()
        if tag == "br":
            node = wn.BrNode()
        elif tag == "hr":
            node = wn.HrNode()
        elif tag == "meta":
            node = wn.MetaNode()
        elif tag == "img":
            node = wn.ImgNode()
        # 赋值标签信息
        node.tag = tag
        node.father = self.now
        # 直接闭合标签必然是有父节点的
        node.index = node.father.index + 1
        node.path = node.father.path + "-" + "{0}[{1}]".format(tag, len(node.father.children) + 1)
        # 给其赋值其属性
        for each in attrs:
            node.attr[each[0]] = each[1]
        # 设定其特别的类型
        node.type = "startendtag"
        # 将其加入其父节点的子节点列表中
        self.now.children.append(node)


    def handle_comment(self, data):
        # 不知道干啥的，看上去是获取注释的，暂时用不到
        HTMLParser.handle_comment(self, data)


    def close(self):
        # 关闭解析
        HTMLParser.close(self)


    def merge_body(self, data = None):
        # 没有参数的话默认是body
        if data == None:
            data = self.body
        # 如果是节点对象，则继续整合其子节点
        if isinstance(data, wn.WebNode):
            self.merge_body(data.children)
        # 如果是list对象，判定其是否有数据
        elif isinstance(data,list) and len(data)>0:
            # 如果只有一个数据，默认不需要合并
            if len(data)==1:
                self.merge_body(data[0])
            # 如果没有一个有子节点
            else:
                # 进行合并操作
                index1 = 0
                index2 = 1
                content = data[index1].content
                while index2 < len(data):
                    # 判定children是否有子节点
                    if len(data[index1].children) > 0 or data[index1].tag not in ['span', 'strong']:
                        index1 += 1
                        index2 = index1 + 1
                        content = data[index1].content
                    elif data[index1].tag == data[index2].tag and len(data[index2].children) == 0: #and data[index1].tag in ['strong', 'span'] :
                        content += data[index2].content
                        index2 += 1
                    else:
                        data[index1].content = content
                        for i in range(index2-index1-1):
                            data.remove(data[index1+1])
                        index1 += 1
                        index2 = index1+1
                        content = data[index1].content
                data[index1].content = content
                for i in range(index2 - index1 - 1):
                    data.remove(data[index1 + 1])
            # 继续递归
            for each in data:
                self.merge_body(each)








if __name__ == "__main__":
    pass
