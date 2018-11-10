import hashlib
import json
import os.path

from flask import Flask, request, abort

from common import file, console, post_map
from manage import post_manage, build_rss, get

app = Flask(__name__)
api_version = 2
system_config = json.loads(file.read_file("./config/system.json"))

console.log("Info", "Loading configuration...")
try:
    password_md5 = json.loads(system_config["API_Password"])["hash_password"]
except (ValueError, KeyError, TypeError):
    console.log("Error", "Check the API_Password configuration items")
    exit(1)
console.log("Success", "load the configuration file successfully!")

def check_password(title, sign):
    hash_md5 = hashlib.md5(str(title + password_md5).encode('utf-8')).hexdigest()
    if sign == hash_md5:
        return True
    return False

@app.route('/control/system_info', methods=['POST'])
def system_info():
    result = dict()
    result["project_name"] = system_config["Project_Name"]
    result["project_description"] = system_config["Project_Description"]
    result["author_image"] = system_config["Author_Image"]
    result["author_name"] = system_config["Author_Name"]
    result["author_introduction"] = system_config["Author_Introduction"]
    result["api_version"] = api_version
    return json.dumps(result)

def select_type(request_type):
    file_url = None
    if request_type == "post":
        file_url = "./config/page.json"
    if request_type == "menu":
        file_url = "./config/menu.json"
    return file_url
@app.route('/control/get_list/<request_type>', strict_slashes=False, methods=['POST'])
def post_list(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    page_list = json.loads(file.read_file(file_url))
    if request_type == "post":
        for item in page_list:
            page_list[page_list.index(item)]["time"] = str(post_map.build_time(item["time"], system_config))
    return json.dumps(page_list)

@app.route('/control/get_content/<request_type>', strict_slashes=False, methods=['POST'])
def get_content(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file(file_url))
    post_id = int(request.json["post_id"])
    result = dict()
    result["title"] = page_list[post_id]["title"]
    result["name"] = page_list[post_id]["name"]
    result["content"] = file.read_file("./document/{0}.md".format(page_list[post_id]["name"]))
    result["status"] = True
    return json.dumps(result)
@app.route('/control/edit/<request_type>', strict_slashes=False, methods=['POST'])
def edit(request_type):
    file_url = select_type(request_type)
    is_menu = False
    if request_type == "menu":
        is_menu = True
    if file_url is None:
        abort(404)
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file(file_url))
    post_id = int(request.json["post_id"])
    name = str(request.json["name"]).replace('/', "").strip()
    title = str(request.json["title"]).strip()
    content = str(request.json["content"])
    sign = str(request.json["sign"])
    status = False
    if page_list[post_id].get("lock", False):
        return json.dumps({"status": False})
    if check_password(title, sign):
        status = True
        config = {"name": name, "title": title}
        post_manage.edit_post(page_list, post_id, config, None, is_menu)
        file.write_file("./document/{0}.md".format(name), content)
        post_manage.update_post()
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name})

@app.route('/control/delete', strict_slashes=False, methods=['POST'])
def delete():
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file("./config/page.json"))
    post_id = int(request.json["post_id"])
    sign = str(request.json["sign"])
    status = False
    if page_list[post_id].get("lock", False):
        return json.dumps({"status": False})
    if check_password(str(post_id) + page_list[post_id]["title"], sign):
        status = True
        post_manage.delete_post(page_list, post_id)
        build_rss.build_rss()
    return json.dumps({"status": status})

@app.route('/control/new', strict_slashes=False, methods=['POST'])
def create_post():
    if request.json is None:
        abort(400)
    title = str(request.json["title"]).strip()
    name = str(request.json["name"]).replace('/', "").strip()
    content = str(request.json["content"])
    sign = str(request.json["sign"])
    status = False
    if len(name) == 0:
        name = get.get_name(title)
    while os.path.exists("./document/{0}.md".format(name)):
        name = "{}-repeat".format(name)
    if check_password(title, sign):
        file.write_file("./document/{0}.md".format(name), content)
        config = {"title": title, "name": name}
        post_manage.new_post(config)
        status = True
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name})

@app.route("/control/git_page_publish", strict_slashes=False, methods=['POST'])
def git_publish():
    from manage import build_static_page
    status = build_static_page.publish()
    return json.dumps({"status": status})
