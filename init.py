import json
import os.path

import memcache
from flask import Flask, abort

from common import file, page, console

rss = None
menu_list = None
restful_switch = False
page_name_list = list()
template_config = None
cache_switch = False
cache_list = list()
cache_page = dict()
app = Flask(__name__)


console.log("info", "Loading configuration")
system_config = json.loads(file.read_file("./config/system.json"))
system_config["API_Password"] = None

page_list = json.loads(file.read_file("./config/page.json"))

if os.path.exists("./config/menu.json"):
    menu_list = json.loads(file.read_file("./config/menu.json"))

if "Restful_API" in system_config:
    if system_config["Restful_API"]:
        restful_switch = True

for item in page_list:
    page_name_list.append(item["name"])

if os.path.exists("./document/rss.xml"):
    rss = file.read_file("document/rss.xml")

if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
    template_config = json.loads(file.read_file("./templates/{0}/config.json".format(system_config["Theme"])))
console.log("Success", "load the configuration file successfully")



# Subscribe
@app.route("/rss")
@app.route("/feed")
def load_rss():
    return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/index/p/<int:page_index>')
@app.route('/index/p/<int:page_index>/')
def route(file_name="index", page_index=1):
    result = None
    get_from_cache = False

    page_index_url=""
    if file_name=="index":
        page_index_url = "/p/{0}".format(str(page_index))
    page_url = "/{0}{1}".format(file_name, page_index_url)

    if page_url in cache_list:
        console.log("info", "Trying to get cache: {0}".format(page_url))
        get_from_cache = True
        result=cache_page[page_url]

    if result is None:
        console.log("info", "Trying to build: {0}".format(page_url))
        if restful_switch:
            result = page.build_restful_result(file_name, system_config, page_list, page_name_list, menu_list)
        else:
            if file_name == "index":
                result, row = page.build_index(page_index, system_config, page_list, menu_list, False, template_config)
            if os.path.exists("document/{0}.md".format(file_name)):
                result = page.build_page(file_name, system_config, page_list, page_name_list, menu_list, False,
                                         template_config)

    if result is not None:
        if not get_from_cache:
            console.log("info", "Writing to cache: {0}".format(page_url))
            cache_list.append(page_url)
            cache_page[page_url]=result
        console.log("Success", "Get success: {0}".format(page_url))
        return result
    console.log("Error", "Can not build: {0}".format(page_url))
    abort(404)
