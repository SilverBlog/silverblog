# coding=utf-8
import hashlib
import json
from flask import Flask, request

from common import file
from manage import new_post, build_rss

app = Flask(__name__)

system_config = json.loads(file.read_file("./config/system.json"))

page_list = json.loads(file.read_file("./config/page.json"))

def check_password(title, encode):
    hash_md5 = hashlib.md5(str(title + system_config["API_Password"]).encode('utf-8')).hexdigest()
    if encode == hash_md5:
        return True
    return False


@app.route('/control/get_post_list', methods=['POST'])
def post_list():
    encode = str(request.json["encode"])
    if check_password("get_post_list", encode):
        for item in page_list:
            page_name_list.append(item["title"])
    return json.dumps(page_name_list)


@app.route('/control/edit', methods=['POST'])
def edit_post():
    post_id = int(request.json["post_id"])
    title = int(request.json["title"])
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    if check_password(post_id, encode):


# todo edit设计
# return json.dumps()
@app.route('/control/new', methods=['POST'])
def new():
    title = str(request.json["title"])
    content = str(request.json["content"])
    encode = str(request.json["encode"])
    state = False
    name = None
    if check_password(title, encode):
        name = new_post.get_name(title)
        file.write_file("./document/{0}.md".format(name), content)
        config = {"title": title, "name": name}
        new_post.new_post_init(config)
        state = True
        build_rss.build_rss()
    return json.dumps({"status": state, "name": name})
