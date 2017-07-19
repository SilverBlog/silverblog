# coding=utf-8

import hashlib
import json
import os

from flask import Flask, request

from common import file
from manage import new_post, build_rss, update_post

app = Flask(__name__)

system_config = json.loads(file.read_file("./config/system.json"))
password_md5 = hashlib.md5(str(system_config["API_Password"]).encode('utf-8')).hexdigest()

if __name__ == '__main__':
    import qrcode_terminal

    if len(system_config["API_Password"]) == 0 or len(system_config["Project_URL"]) == 0:
        print("Check the API_Password and Project_URL configuration items")
        exit()
    print("Please use the client to scan the following QR Code")
    config_json = json.dumps({"url": system_config["Project_URL"], "password": password_md5})
    qrcode_terminal.draw(config_json)
    exit()

def check_password(title, encode):
    if len(system_config["API_Password"]) != 0:
        hash_md5 = hashlib.md5(str(title + password_md5).encode('utf-8')).hexdigest()
        if encode == hash_md5:
            return True
    return False


@app.route('/control/get_post_list', methods=['POST'])
def post_list():
    page_list = json.loads(file.read_file("./config/page.json"))
    page_title_list = list()
    for item in page_list:
        page_title_list.append(item["title"])
    return json.dumps(page_title_list)


@app.route('/control/get_post_content', methods=['POST'])
def get_post_content():
    page_list = json.loads(file.read_file("./config/page.json"))
    post_id = int(request.json["post_id"])
    result = dict()
    result["title"] = page_list[post_id]["title"]
    result["name"] = page_list[post_id]["name"]
    result["content"] = file.read_file("./document/{0}.md".format(page_list[post_id]["name"]))
    result["status"] = True
    return json.dumps(result)


@app.route('/control/edit', methods=['POST'])
def edit_post():
    page_list = json.loads(file.read_file("./config/page.json"))
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
        file.write_file("./config/page.json", json.dumps(page_list))
        file.write_file("./document/{0}.md".format(name), content)
        update_post.update()
        build_rss.build_rss()
    return json.dumps({"status": state, "name": name})


@app.route('/control/delete', methods=['POST'])
def delete_post():
    page_list = json.loads(file.read_file("./config/page.json"))
    post_id = str(request.json["post_id"])
    encode = str(request.json["encode"])
    state = False
    if check_password(post_id, encode):
        state = True
        name = page_list[int(post_id)]["name"]
        del page_list[int(post_id)]
        file.write_file("./config/page.json", json.dumps(page_list))
        os.remove("./document/{0}.md".format(name))
        build_rss.build_rss()
    return json.dumps({"status": state})


@app.route('/control/new', methods=['POST'])
def new():
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


@app.route("/control/git_page_publish")
def git_publish():
    from manage import git_publish
    status = git_publish.git_publish(True)
    return json.dumps({"status": status})
