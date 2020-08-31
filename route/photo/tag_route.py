#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-09-01 0:29
import os, sys, re, json, traceback, time
import _locale
from flask_restful import Resource
from flask import Flask, request, send_file, render_template, send_from_directory
from route.photo.tag import Tag
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


class TagRoute(Resource):
    def get(self):
        delete = request.args.get("delete", None)
        if delete:
            tag = Tag(id=delete)
            tag.delete()

        add = request.args.get("add", None)
        if add:
            tag = Tag(tag_name=add)

        result = Tag.search()
        return render_template("photo/tag.html", result=result)


    def post(self):
        pass


if __name__ == "__main__":
    pass