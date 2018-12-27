import hashlib
import hmac
import json
import os.path
import time

from flask import Flask, request, abort

from common import file, console
from manage import post_manage, build_rss, get

app = Flask(__name__)
api_version = 3
version = "v2"
password_error_counter = 0
total_error_counter = 0
error_time = 0
submit_lock = False
console.log("Info", "Loading configuration...")
system_config = json.loads(file.read_file("./config/system.json"))
control_config = json.loads(file.read_file("./config/control.json"))
password = control_config["password"]
console.log("Success", "load the configuration file successfully!")


def get_index(post_list, post_uuid):
    for item in post_list:
        if item["uuid"] == post_uuid:
            return post_list.index(item)
    return None


def sec_to_ms(timestamp):
    return int(round(timestamp * 1000))


def convert_timestamp(item):
    item["time"] = sec_to_ms(item["time"])
    return item

def check_password(content, sign, send_time):
    global password_error_counter, error_time, submit_lock, total_error_counter
    timestamp = time.time()
    timestamp_ms = sec_to_ms(timestamp)
    elapsed_time = timestamp_ms - send_time
    if elapsed_time > 300000 or elapsed_time < -300000:
        console.log("Error",
                    "Token expired. Time delta between now and expected timestamp is {} ms.".format(elapsed_time))
        abort(408)
    if password_error_counter >= 5:
        submit_lock = True
        if total_error_counter <= 10:
            total_error_counter += 1
        password_error_counter = 0
        error_time = timestamp + (120 * total_error_counter)
    if submit_lock:
        if error_time < timestamp:
            submit_lock = False
        if error_time >= timestamp:
            console.log("Error", "Too many invalid password attempts.")
            abort(403)
    hash_sign = hmac.new(str(password + str(send_time)).encode('utf-8'), str(content).encode('utf-8'),
                         digestmod=hashlib.sha512).hexdigest()
    if sign == hash_sign:
        password_error_counter = 0
        total_error_counter = 0
        return True
    console.log("Error", "Hash error.")
    password_error_counter += 1
    return False


def select_type(request_type):
    file_url = None
    if request_type == "post":
        file_url = "./config/page.json"
    if request_type == "menu":
        file_url = "./config/menu.json"
    return file_url


@app.route('/control/system_info', strict_slashes=False, methods=['GET', 'POST'])
def get_system_info():
    result = dict()
    result["project_name"] = system_config["Project_Name"]
    result["project_description"] = system_config["Project_Description"]
    result["author_image"] = system_config["Author_Image"]
    result["author_name"] = system_config["Author_Name"]
    result["author_introduction"] = system_config["Author_Introduction"]
    result["api_version"] = api_version
    return json.dumps(result)


@app.route('/control/' + version + '/get/list/<request_type>', strict_slashes=False, methods=['GET', 'POST'])
def get_post_list(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    page_list = list(map(convert_timestamp, json.loads(file.read_file(file_url))))
    return json.dumps(page_list)


@app.route('/control/' + version + '/get/content/<request_type>', strict_slashes=False, methods=['POST'])
def get_content(request_type):
    file_url = select_type(request_type)
    if file_url is None:
        abort(404)
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file(file_url))
    post_uuid = str(request.json["post_uuid"])
    post_index = get_index(page_list, post_uuid)
    if post_index is None:
        abort(404)
    result = dict()
    result["title"] = page_list[post_index]["title"]
    result["name"] = page_list[post_index]["name"]
    result["content"] = file.read_file("./document/{0}.md".format(page_list[post_index]["name"]))
    return json.dumps(result)


@app.route('/control/' + version + '/edit/<request_type>', strict_slashes=False, methods=['POST'])
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
    post_uuid = str(request.json["post_uuid"])
    post_index = get_index(page_list, post_uuid)
    if post_index is None:
        abort(404)
    name = str(request.json["name"]).replace('/', "").strip()
    title = str(request.json["title"]).strip()
    content = str(request.json["content"])
    sign = str(request.json["sign"])
    send_time = int(request.json["send_time"])
    status = False
    hash_content = post_uuid + title + name + hashlib.sha512(str(content).encode('utf-8')).hexdigest()
    if check_password(hash_content, sign, send_time):
        status = True
        config = {"name": name, "title": title}
        post_manage.edit_post(page_list, post_index, config, None, is_menu)
        file.write_file("./document/{0}.md".format(name), content)
        post_manage.update_post()
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name})


@app.route('/control/' + version + '/delete', strict_slashes=False, methods=['POST'])
def delete():
    if request.json is None:
        abort(400)
    page_list = json.loads(file.read_file("./config/page.json"))
    post_uuid = str(request.json["post_uuid"])
    post_index = get_index(page_list, post_uuid)
    if post_index is None:
        abort(404)
    sign = str(request.json["sign"])
    send_time = int(request.json["send_time"])
    status = False
    hash_content = page_list[post_index]["uuid"] + page_list[post_index]["title"] + page_list[post_index]["name"]
    if check_password(hash_content, sign, send_time):
        status = True
        post_manage.delete_post(page_list, post_index)
        build_rss.build_rss()
    return json.dumps({"status": status})


@app.route('/control/' + version + '/new', strict_slashes=False, methods=['POST'])
def create_post():
    if request.json is None:
        abort(400)
    title = str(request.json["title"]).strip()
    name = str(request.json["name"]).replace('/', "").strip()
    content = str(request.json["content"])
    sign = str(request.json["sign"])
    send_time = int(request.json["send_time"])
    status = False
    hash_content = title + name + hashlib.sha512(str(content).encode('utf-8')).hexdigest()
    if check_password(hash_content, sign, send_time):
        if len(name) == 0:
            name = get.get_name(title)
        while os.path.exists("./document/{0}.md".format(name)):
            name = "{}-repeat".format(name)
        post_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name)
        file.write_file("./document/{0}.md".format(name), content)
        config = {"title": title, "name": name, "uuid": post_uuid}
        post_manage.new_post(config)
        status = True
        build_rss.build_rss()
    return json.dumps({"status": status, "name": name, "uuid": post_uuid})


@app.route("/control/" + version + "/git_page_publish", strict_slashes=False, methods=['POST'])
def git_publish():
    status = False
    sign = str(request.json["sign"])
    send_time = int(request.json["send_time"])
    if check_password("git_page_publish", sign, send_time):
        from manage import build_static_page
        status = build_static_page.publish()
    return json.dumps({"status": status})
