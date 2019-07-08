import asyncio
import json
import os.path
import time

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
i18n = dict()
static_file_dict = dict()
last_build_year = time.localtime(time.time())[0]
use_redis = False
redis_config = dict()

if os.path.exists("./config/redis.json"):
    try:
        # This package may not exist.
        # noinspection PyUnresolvedReferences
        import redis
    except ImportError:
        console.log("Error", "Please install the [redis] package to support this feature.")


def get_redis_connect(config):
    if config is not None:
        return redis.Redis(host=config["host"], port=config["port"], password=config["password"], db=config["db"])
    return None


@asyncio.coroutine
def async_json_loads(text):
    return json.loads(text)


@asyncio.coroutine
def get_system_config():
    global system_config, template_config, i18n, static_file_dict, redis_config, use_redis
    load_file = yield from file.async_read_file("./config/system.json")
    system_config = yield from async_json_loads(load_file)
    rss_file = None
    if os.path.exists("./document/rss.xml"):
        rss_file = yield from file.async_read_file("./document/rss.xml")

    if os.path.exists("./config/redis.json"):
        redis_config_file = yield from file.async_read_file("./config/redis.json")
        redis_config = yield from async_json_loads(redis_config_file)
        if redis_config is not None:
            use_redis = True
            redis_connect = get_redis_connect(redis_config)
            redis_connect.flushdb()
            if rss_file is not None:
                redis_connect.set("rss", rss_file)
    if not use_redis:
        global rss
        rss = rss_file

    if len(system_config["Theme"]) == 0:
        console.log("Error",
                    "If you do not get the Theme you installed, check your configuration file and the Theme installation.")
        exit(78)

    template_location = "./templates/{0}/".format(system_config["Theme"])
    if os.path.exists(template_location + "config.json"):
        template_config_file = yield from file.async_read_file(template_location + "config.json")
        template_config = yield from async_json_loads(template_config_file)

    if os.path.exists(template_location + "cdn"):
        cdn_config_file = None
        if os.path.exists(template_location + "cdn/custom.json"):
            cdn_config_file = template_location + "cdn/custom.json"
        if cdn_config_file is None:
            cdn_config_file = template_location + "cdn/local.json"
            if system_config["Use_CDN"]:
                cdn_config_file = template_location + "cdn/cdn.json"
        cdn_file = yield from file.async_read_file(cdn_config_file)
        static_file_dict = yield from async_json_loads(cdn_file)

    if os.path.exists(template_location + "i18n"):
        i18n_name = "en-US"
        if "i18n" in system_config and len(system_config["i18n"]) != 0:
            i18n_name = system_config["i18n"]
        i18n_filename = "{0}i18n/{1}.json".format(template_location, i18n_name)
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


def load_config():
    console.log("Info", "Loading configuration...")
    if not os.path.exists("./config/system.json"):
        console.log("Error", "[system.json] file not found.")
        exit(1)
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = [get_system_config(), get_page_list(), get_menu_list()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    global page_list, page_name_list, menu_list, page_list
    for item in page_list:
        page_name_list.append(item["name"])
        page_list[page_list.index(item)]["time_raw"] = item["time"]
        page_list[page_list.index(item)]["time"] = str(post_map.build_time(item["time"], system_config))
    console.log("Success", "load the configuration file successfully!")


app = Flask(__name__, static_folder="templates/static")
load_config()


@app.route("/rss/", strict_slashes=False)
def result_rss():
    global rss
    rss_result = rss
    if use_redis:
        redis_connect = get_redis_connect(redis_config)
        rss_result = redis_connect.get("rss")
    if rss_result is None:
        abort(404)
    return rss_result, 200, {'Content-Type': 'text/xml; charset=utf-8'}


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


def check_build_year():
    global last_build_year
    localtime = time.localtime(time.time())
    if last_build_year != localtime[0]:
        console.log("Info", "Found a year change, cache cleanup.")
        last_build_year = localtime[0]
        cache_index.clear()
        cache_post.clear()


def get_index_cache(page_url):
    check_build_year()
    if use_redis:
        redis_connect = get_redis_connect(redis_config)
        if redis_connect.exists(page_url):
            console.log("Success", "Get redis Success: {0}".format(page_url))
            return redis_connect.get(page_url)
        return None
    if page_url in cache_index:
        console.log("Success", "Get cache Success: {0}".format(page_url))
        return cache_index[page_url]
    return None


def write_index_cache(page_url, content):
    if use_redis:
        redis_connect = get_redis_connect(redis_config)
        redis_connect.set(page_url, content)
        console.log("Info", "Writing to redis: {0}".format(page_url))
        return
    console.log("Info", "Writing to cache: {0}".format(page_url))
    cache_index[page_url] = content


@app.route("/")
@app.route("/index", strict_slashes=False)
@app.route('/index/<int:page_index>', strict_slashes=False)
def index_route(page_index=1):
    page_url = "/index/{0}/".format(page_index)
    result = get_index_cache(page_url)
    if result is None:
        page_row = page.get_page_row(system_config["Paging"], len(page_list))
        if page_index == 0 or page_index > page_row:
            abort(404)
        result = page.build_index(page_index, page_row, system_config, page_list, menu_list, template_config, i18n,
                                  static_file_dict)
    if result is None:
        abort(404)
    write_index_cache(page_url, result)
    console.log("Success", "Get success: {0}".format(page_url))
    return result


def get_post_cache(page_url):
    check_build_year()
    if use_redis:
        redis_connect = get_redis_connect(redis_config)
        if redis_connect.exists(page_url):
            console.log("Success", "Get redis Success: {0}".format(page_url))
            return redis_connect.get(page_url)
        return None
    if page_url in cache_post:
        console.log("Success", "Get cache Success: {0}".format(page_url))
        return cache_post[page_url]
    return None


def write_post_cache(page_url, content):
    if use_redis:
        redis_connect = get_redis_connect(redis_config)
        redis_connect.set(page_url, content)
        console.log("Info", "Writing to redis: {0}".format(page_url))
        return
    if len(cache_post) >= 100:
        page_keys = sorted(cache_post.keys())
        console.log("Info", "Delete cache: {0}".format(page_keys[0]))
        del cache_post[page_keys[0]]
    console.log("Info", "Writing to cache: {0}".format(page_url))
    cache_post[page_url] = content


@app.route("/post/<file_name>")
@app.route("/post/<file_name>/")
def post_route(file_name=None):
    if file_name is None or not os.path.exists("./document/{0}.md".format(file_name)):
        abort(404)
    page_url = "/post/{0}/".format(file_name)
    result = get_post_cache(page_url)
    if result is None:
        page_info = None
        if file_name in page_name_list:
            this_page_index = page_name_list.index(file_name)
            page_info = page_list[this_page_index]
        result = page.build_page(file_name, system_config, page_info, menu_list,
                                 template_config, i18n, static_file_dict)
        write_post_cache(page_url, result)
    console.log("Success", "Get success: {0}".format(page_url))
    return result
