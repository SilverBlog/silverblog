import asyncio
import json
import os.path

from flask import Flask, abort, redirect

from common import file, page, console, post_map

system_config = dict()
page_list = list()
rss = None
menu_list = list()
template_config = dict()
page_name_list = list()
cache_index = dict()
cache_post = dict()

app = Flask(__name__)

console.log("info", "Loading configuration...")
@asyncio.coroutine
def get_system_config():
    global system_config, template_config
    system_config = json.loads(file.read_file("./config/system.json"))
    system_config["API_Password"] = None
    if len(system_config["Theme"]) == 0:
        console.log("Error",
                "If you do not get the Theme you installed, check your configuration file and the Theme installation.")
        exit(1)
    if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
        template_config = json.loads(
            file.read_file("./templates/{0}/config.json".format(system_config["Theme"])))

@asyncio.coroutine
def get_menu_list():
    global menu_list
    menu_list = json.loads(file.read_file("./config/menu.json"))


@asyncio.coroutine
def get_page_list():
    global page_list
    page_list = json.loads(file.read_file("./config/page.json"))
@asyncio.coroutine
def get_rss():
    global rss
    if os.path.exists("./document/rss.xml"):
        rss = file.read_file("document/rss.xml")

loop = asyncio.get_event_loop()
tasks = [get_system_config(), get_page_list(), get_menu_list(), get_rss()]
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

for item in page_list:
    page_name_list.append(item["name"])
    page_list[page_list.index(item)]["time"] = str(post_map.build_time(item["time"], system_config))
menu_list = list(map(post_map.add_post_header, menu_list))
page_list = list(map(post_map.add_post_header, page_list))
console.log("Success", "load the configuration file successfully!")

@app.route("/rss/", strict_slashes=False)
@app.route("/feed/", strict_slashes=False)
def result_rss():
    if rss is None:
        abort(404)
    return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route("/static/")
def static_file():
    abort(400)

@app.route("/")
@app.route("/index", strict_slashes=False)
@app.route('/index/p/<int:page_index>', strict_slashes=False)
def index_route(page_index=1):
    page_url = "/index/p/{0}/".format(page_index)
    if page_url in cache_index:
        console.log("info", "Get cache Success: {0}".format(page_url))
        return cache_index[page_url]

    console.log("info", "Trying to build: {0}".format(page_url))
    result, row = page.build_index(page_index, system_config, page_list, menu_list,
                                   False, template_config)

    console.log("info", "Writing to cache: {0}".format(page_url))
    if len(cache_index) >= 100:
        page_keys = sorted(cache_index.keys())
        console.log("info", "Delete cache: {0}".format(page_keys[0]))
        del cache_index[page_keys[0]]
    cache_index[page_url] = result
    console.log("Success", "Get success: {0}".format(page_url))

    return result


@app.route("/<file_name>", strict_slashes=False)
def redirect_301(file_name):
    if file_name in page_name_list or os.path.exists("document/{0}.md".format(file_name)):
        return redirect("/post/{0}/".format(file_name), code=301)
    abort(404)


@app.route("/post/<file_name>")
@app.route("/post/<file_name>/")
def post_route(file_name=None):
    if file_name is None or not os.path.exists("document/{0}.md".format(file_name)):
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
                             False,
                             template_config)
    console.log("info", "Writing to cache: {0}".format(page_url))
    if len(cache_post) >= 100:
        page_keys = sorted(cache_post.keys())
        console.log("info", "Delete cache: {0}".format(page_keys[0]))
        del cache_post[page_keys[0]]
    cache_post[page_url] = result
    console.log("Success", "Get success: {0}".format(page_url))

    return result

