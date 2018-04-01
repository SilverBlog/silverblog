import requests

def get(url):
    r = requests.get("http://127.0.0.1/" + url)
    if r.status_code == 200:
        return True
    return False
def post(url):
    r = requests.post("http://127.0.0.1/" + url)
    if r.status_code == 200:
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

r = requests.post("http://127.0.0.1/control/get_content/post", json={"post_id": 0})
print("get_content:" + r.text)
if not r.json()["status"]:
    print("ERROR:get_content")
    exit(1)

r = requests.post("http://127.0.0.1/control/new", json={"content": "test", "name": "test", "title": "title",
                                                        "sign": "bd35db586ff3f4617d90511546aa6e3b"})
print("new:" + r.text)
if not r.json()["status"]:
    print("ERROR:new")
    exit(1)

r = requests.post("http://127.0.0.1/control/edit/post",
                  json={"post_id": 0, "content": "test2", "name": "test", "title": "title",
                        "sign": "bd35db586ff3f4617d90511546aa6e3b"})
print("edit:" + r.text)
if not r.json()["status"]:
    print("ERROR:edit")
    exit(1)
r = requests.post("http://127.0.0.1/control/delete", json={"post_id": 0, "sign": "f48659e554318cf884d0edbc7038c52c"})
print("delete:" + r.text)
if not r.json()["status"]:
    print("ERROR:delete")
    exit(1)
