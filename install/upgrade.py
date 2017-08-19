import json


def read_file(filename):
    f = open(filename, newline=None)
    content = f.read()
    return content


def write_file(filename, content):
    f = open(filename, "w", newline=None)
    f.write(content)
    f.close()
    return True


menu = json.loads(read_file("../config/menu.json"))
new_menu = list()
for item in menu:
    new_item = dict()
    new_item["title"] = item["name"]
    new_item["name"] = item["url"]
    if "absolute" in item:
        new_item["absolute"] = item["absolute"]
    new_menu.append(new_item)
write_file("../config/menu.json", json.dumps(new_menu))
