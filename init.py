# -*- coding: utf-8 -*-
import asyncio
import json
import os.path

from flask import Flask, abort, redirect, request

from common import file, page, console, post_map

system_config = dict()
page_list = list()
rss = None
menu_list = list()
template_config = dict()
page_name_list = list()
cache_index = dict()
cache_post = dict()
i18n = dict()

@asyncio.coroutine
def async_json_loads(text):
    return json.loads(text)

@asyncio.coroutine
def get_system_config():
    global system_config, template_config, i18n
    load_file = yield from file.async_read_file("./config/system.json")
    system_config = yield from async_json_loads(load_file)
    del system_config["API_Password"]
    if len(system_config["Theme"]) == 0:
        console.log("Error",
                    "If you do not get the Theme you installed, check your configuration file and the Theme installation.")
        exit(1)
    if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
        template_config_file = yield from file.async_read_file(
            "./templates/{0}/config.json".format(system_config["Theme"]))
        template_config = yield from async_json_loads(template_config_file)
    if os.path.exists("./templates/{}/i18n".format(system_config["Theme"])):
        i18n_name = "en-US"
        if "i18n" in system_config and len(system_config["i18n"]) != 0:
            i18n_name = system_config["i18n"]
        i18n_filename = "./templates/{0}/i18n/{1}.json".format(system_config["Theme"], i18n_name)
        if os.path.exists(i18n_filename):
            i18n_file = yield from file.async_read_file(i18n_filename)
            i18n = yield from async_json_loads(i18n_file)

@asyncio.coroutine
def get_menu_list():
    global menu_list
    load_file = yield from file.async_read_file("./config/menu.json")
    menu_list = yield from async_json_loads(load_file)

@asyncio.coroutine
def get_page_list():
    global page_list
    load_file = yield from file.async_read_file("./config/page.json")
    page_list = yield from async_json_loads(load_file)

@asyncio.coroutine
def get_rss_file():
    global rss
    if os.path.exists("./document/rss.xml"):
        rss = yield from file.async_read_file("./document/rss.xml")
def load_config():
    console.log("info", "Loading configuration...")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = [get_system_config(), get_page_list(), get_menu_list(), get_rss_file()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    global page_list, page_name_list, menu_list, page_list
    for item in page_list:
        page_name_list.append(item["name"])
        page_list[page_list.index(item)]["time"] = str(post_map.build_time(item["time"], system_config))
    menu_list = list(map(post_map.add_post_header, menu_list))
    page_list = list(map(post_map.add_post_header, page_list))
    console.log("Success", "load the configuration file successfully!")

def check_proxy_ip(header):
    if 'X-Real-Ip' in header:
        console.log("ClientIP", "X-Real-IP is :" + header['X-Real-Ip'])

app = Flask(__name__)
load_config()

@app.route("/rss/", strict_slashes=False)
def result_rss():
    check_proxy_ip(request.headers)
    if rss is None:
        abort(404)
    return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}

@app.route("/static/")
def static_file():
    abort(400)

@app.route("/<file_name>/p/<int:page_index>", strict_slashes=False)
@app.route("/<file_name>", strict_slashes=False)
def redirect_301(file_name, page_index=1):
    if file_name == "index":
        return redirect("/index/{}".format(page_index), code=301)
    if file_name in ('rss.xml', "feed.xml", "atom.xml", "feed", "atom"):
        return redirect("/rss", code=301)
    if file_name in page_name_list or os.path.exists("./document/{0}.md".format(file_name)):
        return redirect("/post/{0}/".format(file_name), code=301)
    abort(404)

@app.route("/")
@app.route("/index", strict_slashes=False)
@app.route('/index/<int:page_index>', strict_slashes=False)
def index_route(page_index=1):
    check_proxy_ip(request.headers)
    page_url = "/index/{0}/".format(page_index)
    if page_url in cache_index:
        console.log("info", "Get cache Success: {0}".format(page_url))
        return cache_index[page_url]
    console.log("info", "Trying to build: {0}".format(page_url))
    page_row = page.get_page_row(system_config["Paging"], len(page_list))
    if page_index == 0 or page_index > page_row:
        abort(404)
    result = page.build_index(page_index, page_row, system_config, page_list, menu_list, template_config, i18n)
    if result is None:
        abort(404)
    console.log("info", "Writing to cache: {0}".format(page_url))
    if len(cache_index) >= 50:
        page_keys = sorted(cache_index.keys())
        console.log("info", "Delete cache: {0}".format(page_keys[0]))
        del cache_index[page_keys[0]]
    cache_index[page_url] = result
    console.log("Success", "Get success: {0}".format(page_url))
    return result

@app.route("/post/<file_name>")
@app.route("/post/<file_name>/")
def post_route(file_name=None):
    check_proxy_ip(request.headers)
    if file_name is None or not os.path.exists("./document/{0}.md".format(file_name)):
        abort(404)
    page_url = "/post/{0}/".format(file_name)
    if page_url in cache_post:
        console.log("info", "Get cache Success: {0}".format(page_url))
        return cache_post[page_url]
    page_info = None
    if file_name in page_name_list:
        this_page_index = page_name_list.index(file_name)
        page_info = page_list[this_page_index]
    result = page.build_page(file_name, system_config, page_info, menu_list,
                             template_config, i18n)
    console.log("info", "Writing to cache: {0}".format(page_url))
    if len(cache_post) >= 50:
        page_keys = sorted(cache_post.keys())
        console.log("info", "Delete cache: {0}".format(page_keys[0]))
        del cache_post[page_keys[0]]
    cache_post[page_url] = result
    console.log("Success", "Get success: {0}".format(page_url))

    return result