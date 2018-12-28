import hashlib
import hmac
import time

import requests

host = "http://127.0.0.1/"
time.sleep(2)
def get(url):
    r = requests.get(host + url)
    if r.status_code != 200:
        print(r.status_code)
        exit(1)


def build_hash(password, content, send_time):
    return hmac.new(str(password + str(send_time)).encode('utf-8'), str(content).encode('utf-8'),
                    digestmod=hashlib.sha512).hexdigest()


get_list = ["", "post/demo-article", "rss", "control/system_info", "control/v2/get/list/post",
            "control/v2/get/list/menu"]
for item in get_list:
    get(item)

password_hash = "a238f3ead3fcf2df15e43e0558b5cc374ede284e17a6f03c396a5014606e6901"
r = requests.post(host + "control/v2/get/content/post", json={"post_uuid": "c3472075-440f-42d9-9421-3e83d46568d4"})
print("get_content:" + r.text)
if not r.json()["status"]:
    print("ERROR:get_content")
    exit(1)

name = "test"
title = "test_title"
content = "this is a test"

sign_text = title + name + hashlib.sha512(content.encode("utf-8")).hexdigest()
send_time = int(round(time.time() * 1000))
sign = build_hash(password_hash, sign_text, send_time)
r = requests.post(host + "control/v2/new", json={"content": content, "name": name, "title": title,
                                                  "sign": sign, "send_time": send_time})
print("new:" + r.text)
if not r.json()["status"]:
    print("ERROR:new")
    exit(1)

new_uuid = r.json()["uuid"]
name = "test2"
title = "test2_title"
content = "this is a test2"
sign_text = new_uuid + title + name + hashlib.sha512(content.encode("utf-8")).hexdigest()
send_time = int(round(time.time() * 1000))
sign = build_hash(password_hash, sign_text, send_time)

r = requests.post(host + "control/v2/edit/post",
                  json={"post_uuid": new_uuid, "content": content, "name": name, "title": title,
                        "sign": sign, "send_time": send_time})
print("edit:" + r.text)
if not r.json()["status"]:
    print("ERROR:edit")
    exit(1)

sign_text = new_uuid + title + name
send_time = int(round(time.time() * 1000))
sign = build_hash(password_hash, sign_text, send_time)
r = requests.post(host + "control/v2/delete", json={"post_uuid": new_uuid, "sign": sign, "send_time": send_time})
print("delete:" + r.text)
if not r.json()["status"]:
    print("ERROR:delete")
    exit(1)
exit(0)
