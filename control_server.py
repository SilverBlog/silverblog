# coding=utf-8

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import hashlib
import json
import os

from flask import Flask, request, abort

from common import file, console
from manage import new_post, build_rss, update_post

app = Flask(__name__)

system_config = json.loads(file.read_file("./config/system.json"))
password_md5 = hashlib.md5(str(system_config["API_Password"]).encode('utf-8')).hexdigest()

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
    if len(system_config["API_Password"]) != 0:
        hash_md5 = hashlib.md5(str(title + password_md5).encode('utf-8')).hexdigest()
        if encode == hash_md5:
            return True
    return False


@app.route('/control/system_info', methods=['POST', 'GET'])
def system_info():
    result = dict()
    result["project_name"] = system_config["Project_Name"]
    result["project_description"] = system_config["Project_Description"]
    result["author_image"] = system_config["Author_Image"]
    result["author_name"] = system_config["Author_Name"]
    result["author_introduction"] = system_config["Author_Introduction"]
    return json.dumps(result)


def select_type(request_type):
    file_url = None
    if request_type == "post":
        file_url = "./config/page.json"
    if request_type == "menu":
        file_url = "./config/menu.json"
    return file_url

@app.route('/control/get_<request_type>_list', methods=['POST', 'GET'])
def post_list(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    return file.read_file(file_url)


@app.route('/control/get_<request_type>_content', methods=['POST', 'GET'])
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


@app.route('/control/edit_<request_type>', methods=['POST'])
def edit_post(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file(file_url))
    post_id = str(request.json["post_id"])
    name = str(request.json["name"])
    title = str(request.json["title"])
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    state = False
    if check_password(title, encode):
        state = True
        page_list[int(post_id)]["title"] = title
        if page_list[int(post_id)]["name"] is not name:
            os.remove("./document/{0}.md".format(page_list[int(post_id)]["name"]))
            page_list[int(post_id)]["name"] = name
        file.write_file(file_url, json.dumps(page_list))
        file.write_file("./document/{0}.md".format(name), content)
        if not "menu" in request.json or not request.json["menu"]:
            update_post.update()
            build_rss.build_rss()
    return json.dumps({"status": state, "name": name})


@app.route('/control/delete', methods=['POST'])
def delete_post():
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file("./config/page.json"))
    post_id = str(request.json["post_id"])
    encode = str(request.json["encode"])
    state = False
    if check_password(post_id + page_list[int(post_id)]["title"], encode):
        state = True
        name = page_list[int(post_id)]["name"]
        del page_list[int(post_id)]
        file.write_file("./config/page.json", json.dumps(page_list))
        os.remove("./document/{0}.md".format(name))
        build_rss.build_rss()
    return json.dumps({"status": state})


@app.route('/control/new', methods=['POST'])
def new():
    if request.json is None:
        abort(400)
    title = str(request.json["title"])
    name = str(request.json["name"])
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    state = False
    if check_password(title, encode):
        if len(name) == 0:
            name = new_post.get_name(title)
        file.write_file("./document/{0}.md".format(name), content)
        config = {"title": title, "name": name}
        new_post.new_post_init(config)
        state = True
        build_rss.build_rss()
    return json.dumps({"status": state, "name": name})


@app.route("/control/git_page_publish", methods=['POST'])
def git_publish():
    from manage import git_publish
    status = git_publish.git_publish(False)
    return json.dumps({"status": status})
