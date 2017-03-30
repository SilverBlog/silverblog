#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import os.path

import memcache
from flask import Flask, abort

from common import file, page

# Global Var
system_config = None
menu_list = None
rss = None
restful_switch = False
page_name_list = list()
template_config = None
cache_switch = False
page_list = None
mc = None
app = Flask(__name__)


@app.route('/manage/reload_config')
def load_config():
    global system_config, menu_list, rss, restful_switch, page_name_list, template_config, cache_switch, mc, page_list
    system_config = json.loads(file.read_file("config/system.json"))
    system_config["API_Password"] = None

    page_list = json.loads(file.read_file("./config/page.json"))

    if os.path.exists("./config/menu.json"):
        menu_list = json.loads(file.read_file("./config/menu.json"))

    if os.path.exists("document/rss.xml"):
        rss = file.read_file("document/rss.xml")

    if "Restful_API" in system_config:
        if system_config["Restful_API"]:
            restful_switch = True

    for item in page_list:
        page_name_list.append(item["name"])

    cache_switch = system_config["Cache"]
    if cache_switch:
        mc = memcache.Client([system_config["Memcached_Connect"]], socket_timeout=500, debug=0)
        mc.flush_all()

    if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
        template_config = json.loads("./templates/{0}/config.json".format(system_config["Theme"]))
    return "Reload the configuration file successfully"

load_config()

# Subscribe
@app.route("/rss")
@app.route("/feed")
def rss():
    return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/<file_name>/p/<page_index>')
@app.route('/<file_name>/p/<page_index>/')
def route(file_name="index", page_index="1"):
    result = None

    if cache_switch:
        result = mc.get("{0}/p/{1}".format(file_name, str(page_index)))

    if restful_switch and result is None:
        result = page.build_restful_result(file_name, system_config, page_list, page_name_list, menu_list)

    if result is None:
        if file_name == "index":
            result, row = page.build_index(int(page_index), system_config, page_list, menu_list, False, template_config)
        if os.path.exists("document/{0}.md".format(file_name)):
            result = page.build_page(file_name, system_config, page_list, page_name_list, menu_list, False,
                                     template_config)

    if result is not None:
        if cache_switch:
            mc.set("{0}/p/{1}".format(file_name, str(page_index)), result)
        return result
    abort(404)
