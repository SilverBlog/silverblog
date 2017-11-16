import json
import os.path

from common import file, console
from manage import get_excerpt

def update():
    page_list_file = json.loads(file.read_file("./config/page.json"))
    page_list = page_list_file
    remove_list = list()
    for item in page_list:
        processing_file = "./document/{0}.md".format(item["name"])
        if not os.path.exists(processing_file):
            remove_list.append(item["name"])
        else:
            console.log("Build", "Processing file: {0}".format(processing_file))
            item["excerpt"] = get_excerpt.get_excerpt(processing_file)

    for item in range(len(page_list) - 1, -1, -1):
        if page_list[item]["name"] in remove_list:
            console.log("Remove", "Removing from list: {0}".format(page_list[item]["name"]))
            page_list.pop(item)
    if page_list_file != page_list:
        file.write_file("./config/page.json", json.dumps(page_list, ensure_ascii=False, indent=4, sort_keys=False))

    console.log("Success", "Update article metadata is successful!")
