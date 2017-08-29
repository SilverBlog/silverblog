import json
import os.path

from flask import Flask, abort

from common import file, page, console

rss = None
menu_list = None
page_name_list = list()
cache_page = dict()
template_config = None
app = Flask(__name__)

console.log("info", "Loading configuration")

system_config = json.loads(file.read_file("./config/system.json"))

if system_config["Author_Image"] == "" and system_config["Author_Name"] != "":
    import request
    r = request.get("https://en.gravatar.com/{0}.json".formart(system_config["Author_Name"]))
    if r.status_code == 200:
        req = r.json()
        gravatar_hash = req["entry"]["hash"]
        system_config["Author_Image"] = "https://secure.gravatar.com/avatar/{0}".format(gravatar_hash)
        file.write_file("./config/system.json", json.dumps(system_config))

page_list = json.loads(file.read_file("./config/page.json"))

if os.path.exists("./config/menu.json"):
    menu_list = json.loads(file.read_file("./config/menu.json"))

for item in page_list:
    page_name_list.append(item["name"])

if os.path.exists("./document/rss.xml"):
    rss = file.read_file("document/rss.xml")

if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
    template_config = json.loads(file.read_file("./templates/{0}/config.json".format(system_config["Theme"])))

system_config["API_Password"] = None

console.log("Success", "load the configuration file successfully")


# Subscribe
@app.route("/rss")
@app.route("/feed")
def load_rss():
    if rss is None:
        abort(404)
    return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route("/static/")
def static_file():
    abort(400)

@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/<file_name>/p/<int:page_index>')
@app.route('/<file_name>/p/<int:page_index>/')
def route(file_name="index", page_index=1):
    result = None

    page_index_url = ""
    if file_name == "index":
        page_index_url = "/p/{0}".format(str(page_index))
    page_url = "/{0}{1}".format(file_name, page_index_url)

    if page_url in cache_page:
        console.log("info", "Get cache Success: {0}".format(page_url))
        return cache_page[page_url]

    console.log("info", "Trying to build: {0}".format(page_url))

    if system_config["Restful_API"]:
        result = page.build_restful_result(file_name, system_config, page_list, page_name_list, menu_list)

    if result is None:
        if file_name == "index":
            result, row = page.build_index(page_index, system_config, page_list, menu_list, False, template_config)
        if os.path.exists("document/{0}.md".format(file_name)):
            result = page.build_page(file_name, system_config, page_list, page_name_list, menu_list, False,
                                     template_config)

    if result is not None:
        console.log("info", "Writing to cache: {0}".format(page_url))
        if len(cache_page) >= 2:
            del cache_page[cache_page.keys()[0]]
        cache_page[page_url] = result
        console.log("Success", "Get success: {0}".format(page_url))

        return result

    console.log("Error", "Can not build: {0}".format(page_url))
    abort(404)
