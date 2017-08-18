import json

from common import file

menu = json.loads(file.read_file("../config/menu.json"))
new_menu = list()
for item in menu:
    new_item = dict()
    new_item["title"] = item["name"]
    new_item["name"] = item["url"]
    new_menu.append(new_item)
file.write_file("../config/menu.json", json.dumps(new_menu))
