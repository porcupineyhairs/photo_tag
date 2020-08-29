#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2019/5/17 下午3:13
import os, sys, re, json, traceback
from app import app as flask_app
from flask_restful import Resource,Api

api = Api(flask_app)

# @app.route('/aaa', methods=['GET'])
def extract_html():
    return "123123123asdfasdfasdf"

api.add_resource(extract_html,'/aaa')
if __name__ == "__main__":
    pass
