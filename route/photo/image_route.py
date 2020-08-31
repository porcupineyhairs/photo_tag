#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-08-31 23:46
import os, sys, re, json, traceback, time
import _locale
from flask_restful import Resource
from flask import Flask, request, send_file, render_template, send_from_directory

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

class ImageRoute(Resource):
    def get(self):
        # 这里就需要考虑多维度的查询问题了
        # tag查询   日期查询   时间正序倒序
        pass

    def post(self):
        pass


if __name__ == "__main__":
    pass