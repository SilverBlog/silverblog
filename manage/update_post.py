import json
import os.path

from common import file, get_excerpt
from manage import get_excerpt


def update():
    page_list = json.loads(file.read_file("./config/page.json"))
    remove_list = list()
    for item in page_list:
        if not os.path.isfile("./document/" + item["name"] + ".md"):
            remove_list.append(item["name"])
        else:
            item["excerpt"] = get_excerpt.get_excerpt("./document/" + item["name"] + ".md")

    for item in range(len(page_list) - 1, -1, -1):
        if page_list[item]["name"] in remove_list:
            page_list.pop(item)

    file.write_file("./config/page.json", json.dumps(page_list, ensure_ascii=False))
    print("Update article metadata is successful!")
