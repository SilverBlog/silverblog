#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import os.path

import memcache
from flask import Flask, abort

from common import file,page,markdown


def restful_result(name):
    content = None
    page_info = None
    if name != "index":
        content = file.read_file("document/{0}.md".format(name))
        if name in page_name_list:
            page_info = page_list[page_name_list.index(name)]
        else:
            if os.path.exists("document/{0}.json".format(name)):
                page_info = json.loads(file.read_file("document/{0}.json".format(name)))
            else:
                page_info = {"title": "undefined"}
        content = markdown.markdown(content)
    result = {"menu_list": menu_list, "page_list": page_list, "system_config": system_config, "page_info": page_info,
              "content": content}
    return json.dumps(result, ensure_ascii=False)


app = Flask(__name__)
page_list = json.loads(file.read_file("./config/page.json"))
system_config = json.loads(file.read_file("config/system.json"))
system_config["API_Password"] = None
if os.path.exists("./config/menu.json"):
    menu_list = json.loads(file.read_file("./config/menu.json"))

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
    mc = memcache.Client([system_config["Memcached_Connect"]], socket_timeout=500, debug=0)
    mc.flush_all()


# 分组页面
@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/<file_name>/p/<page_index>')
@app.route('/<file_name>/p/<page_index>/')
def route(file_name="index", page_index="1"):
    if file_name == "rss" or file_name == "feed":
        return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}

    if cache_switch:
        cache_result = mc.get("{0}/p/{1}".format(file_name, str(page_index)))
        if cache_result is not None:
            return cache_result

    if restful_switch:
        result = restful_result(file_name)
    else:
        if file_name == "index":
            result, row = page.build_index(int(page_index), system_config, page_list, menu_list, False)
        elif os.path.exists("document/{0}.md".format(file_name)):
            result = page.build_page(file_name, system_config, page_list, page_name_list, menu_list, False)
        else:
            result = None
    if result is not None:
        if cache_switch:
            mc.set("{0}/p/{1}".format(file_name, str(page_index)), result)
        return result
    else:
        abort(404)
