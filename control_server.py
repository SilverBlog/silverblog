# coding=utf-8

import hashlib
import json
import os.path

from flask import Flask, request, abort

from common import file, console, post_map
from manage import new_post, build_rss, update_post, build_static_page, delete_post, edit_post

app = Flask(__name__)
api_version = 2
system_config = json.loads(file.read_file("./config/system.json"))

console.log("info", "Loading configuration...")
try:
    password_md5 = json.loads(system_config["API_Password"])["hash_password"]
except (ValueError, KeyError, TypeError):
    if len(system_config["API_Password"]) == 0:
        exit(1)
    password_md5 = hashlib.md5(str(system_config["API_Password"]).encode('utf-8')).hexdigest()
    system_config["API_Password"] = json.dumps({"hash_password": password_md5})
    file.write_file("./config/system.json", json.dumps(system_config, indent=4, sort_keys=False, ensure_ascii=False))
console.log("Success", "load the configuration file successfully!")
if __name__ == '__main__':
    try:
        import qrcode_terminal
    except ImportError:
        console.log("Error", "Please install the qrcode-terminal package to support this feature")
        exit(1)
    if len(system_config["API_Password"]) == 0 or len(system_config["Project_URL"]) == 0:
        print("Check the API_Password and Project_URL configuration items")
        exit(1)
    print("Please use the client to scan the following QR Code")
    config_json = json.dumps({"url": system_config["Project_URL"], "password": password_md5})
    qrcode_terminal.draw(config_json)
    exit(0)

def check_password(title, encode):
    hash_md5 = hashlib.md5(str(title + password_md5).encode('utf-8')).hexdigest()
    if encode == hash_md5:
        return True

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
@app.route('/control/get_<request_type>_list', strict_slashes=False, methods=['POST'])
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
@app.route('/control/get_<request_type>_content', strict_slashes=False, methods=['POST'])
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
@app.route('/control/edit_<request_type>', strict_slashes=False, methods=['POST'])
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
    post_id = str(request.json["post_id"])
    name = str(request.json["name"]).replace('/', "")
    title = str(request.json["title"])
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    status = False
    if page_list[int(post_id)].get("protection", False):
        return json.dumps({"status": False})
    if check_password(title, encode):
        status = True
        config = {"name": name, "title": title}
        edit_post.edit(page_list, int(post_id), config, None, is_menu)
        file.write_file("./document/{0}.md".format(name), content)
        update_post.update()
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name})

@app.route('/control/delete', strict_slashes=False, methods=['POST'])
def delete():
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file("./config/page.json"))
    post_id = str(request.json["post_id"])
    encode = str(request.json["encode"])
    status = False
    if page_list[int(post_id)].get("protection", False):
        return json.dumps({"status": False})
    if check_password(post_id + page_list[int(post_id)]["title"], encode):
        status = True
        delete_post.delete(page_list, int(post_id))
        build_rss.build_rss()
    return json.dumps({"status": status})

@app.route('/control/new', strict_slashes=False, methods=['POST'])
def new():
    if request.json is None:
        abort(400)
    title = str(request.json["title"])
    name = str(request.json["name"]).replace('/', "")
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    status = False
    if len(name) == 0:
        name = new_post.get_name(title)
    while os.path.exists("./document/{0}.md".format(name)):
        name = "{}-repeat".format(name)
    if check_password(title, encode):
        file.write_file("./document/{0}.md".format(name), content)
        config = {"title": title, "name": name}
        new_post.new_post_init(config)
        status = True
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name})

@app.route("/control/git_page_publish", strict_slashes=False, methods=['POST'])
def git_publish():
    status = build_static_page.publish(True, False)
    return json.dumps({"status": status})
