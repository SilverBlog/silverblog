import subprocess
import time

import requests

main_progress = subprocess.Popen(["python3", "watch.py", "--debug"])
control_progress = subprocess.Popen(["python3", "watch.py", "--control", "--debug"])
nginx_progress = subprocess.Popen("nginx")
host = "http://127.0.0.1/"
time.sleep(5)
def get(url):
    r = requests.get(host + url)
    if r.status_code == 200:
        print(url + ":" + r.text)
        return True
    return False
def post(url):
    r = requests.post(host + url)
    if r.status_code == 200:
        print(url + ":" + r.text)
        return True
    return False

get_list = ["", "post/demo-article", "rss"]
for item in get_list:
    if not get(item):
        print("ERROR:" + item)
        exit(1)

post_list = ["control/system_info", "control/get_list/post", "control/get_list/menu"]
for item in post_list:
    if not post(item):
        print("ERROR:" + item)
        exit(1)

r = requests.post(host + "/control/get_content/post", json={"post_id": 0})
print("get_content:" + r.text)
if not r.json()["status"]:
    print("ERROR:get_content")
    exit(1)

r = requests.post(host + "/control/new", json={"content": "test", "name": "test", "title": "title",
                                                        "sign": "bd35db586ff3f4617d90511546aa6e3b"})
print("new:" + r.text)
if not r.json()["status"]:
    print("ERROR:new")
    exit(1)

r = requests.post(host + "/control/edit/post",
                  json={"post_id": 0, "content": "test2", "name": "test", "title": "title",
                        "sign": "bd35db586ff3f4617d90511546aa6e3b"})
print("edit:" + r.text)
if not r.json()["status"]:
    print("ERROR:edit")
    exit(1)
r = requests.post(host + "/control/delete", json={"post_id": 0, "sign": "f48659e554318cf884d0edbc7038c52c"})
print("delete:" + r.text)
if not r.json()["status"]:
    print("ERROR:delete")
    exit(1)
nginx_progress.kill()
main_progress.kill()
control_progress.kill()
exit(0)
