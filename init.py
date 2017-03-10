#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import os.path

import memcache
from flask import Flask, abort, render_template

from common import file
from common import markdown

app = Flask(__name__)

# 分组页面
@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/<file_name>/p/<page>')
@app.route('/<file_name>/p/<page>/')
def route(file_name="index", page="1"):
    cache_pagename = file_name
    cache_result = get_cache("{0}/p/{1}".format(cache_pagename, str(page)))
    if cache_result is not None:
        return cache_result
    if file_name == "index":
        return build_index(int(page))
    if file_name == "rss" or file_name == "feed":
        return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    if os.path.isfile("document/{0}.md".format(file_name)):
        return build_page(file_name)
    else:
        abort(404)


def build_index(page):
    page_info = {"title": "index"}
    if restful_switch:
        result = {"menu_list": menu_list, "page_list": page_list, "system_config": system_config}
        result = json.dumps(result)
    else:
        Start_num = -system_config["Paging"] + (int(page) * system_config["Paging"])
        page_row_mod = divmod(len(page_list), system_config["Paging"])
        if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
            page_row = page_row_mod[0] + 1
        else:
            page_row = page_row_mod[0]
        if page <= 0:
            abort(404)
        index_list = page_list[Start_num:Start_num + system_config["Paging"]]
        result = render_template("./{0}/index.html".format(system_config["Theme"]), menu_list=menu_list,
                                 page_list=index_list,
                                 page_info=page_info,
                                 system_config=system_config,
                                 page_row=page_row,
                                 now_page=page, last_page=page - 1, next_page=page + 1,static=False)
    set_cache("index/p/{0}".format(str(page)), result)
    return result


def build_page(name):
    Document_Raw = file.read_file("document/{0}.md".format(name))
    if name in page_name_list:
        page_info = page_list[page_name_list.index(name)]
        content = Document_Raw
    else:
        Documents = Document_Raw.split("<!--infoend-->")
        page_info = json.loads(Documents[0])
        content = Documents[1]
    document = markdown.markdown(content)
    if restful_switch:
        result = {"menu_list": menu_list, "page_info": page_info,
                  "system_config": system_config, "content": document}
        result = json.dumps(result)
    else:
        result = render_template("./{0}/post.html".format(system_config["Theme"]),
                                 page_info=page_info, menu_list=menu_list, content=document,
                                 system_config=system_config,static=False)
    set_cache("{0}/p/1".format(name), result)
    return result

def get_cache(page_name):
    if cache_switch:
        return mc.get(page_name)
    else:
        return None

def set_cache(page_name, content):
    if cache_switch:
        mc.set(page_name, content)


page_list = json.loads(file.read_file("./config/page.json"))
menu_list = json.loads(file.read_file("./config/menu.json"))
system_config = json.loads(file.read_file("config/system.json"))

rss = None
if os.path.exists("document/rss.xml"):
    rss = file.read_file("document/rss.xml")

restful_switch = False

if "Restful_API" in system_config:
    if system_config["Restful_API"]:
        restful_switch = True

page_name_list = list()
for item in page_list:
    page_name_list.append(item["name"])

cache_switch = system_config["Cache"]
if cache_switch:
    try:
        mc = memcache.Client([system_config["Memcached_Connect"]], debug=0)
        mc.flush_all()
    except:
        cache_switch = False
