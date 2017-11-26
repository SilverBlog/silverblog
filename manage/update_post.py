import json
import os.path

from common import file, console
from manage import get_excerpt

def update():
    page_list_file = json.loads(file.read_file("./config/page.json"))
    page_list =list()

    for item in page_list_file:
        processing_file = "./document/{0}.md".format(item["name"])
        hit_file=False
        if os.path.exists(processing_file):
            hit_file=True
            console.log("Build", "Processing file: {0}".format(processing_file))
            item["excerpt"] = get_excerpt.get_excerpt(processing_file)
            page_list.append(item)
        if not hit_file:
            console.log("Remove", "Removing from list: {0}".format(processing_file))

    file.write_file("./config/page.json", json.dumps(page_list, ensure_ascii=False, indent=4, sort_keys=False))
    console.log("Success", "Update article metadata is successful!")
    return True
