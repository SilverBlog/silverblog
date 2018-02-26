import asyncio
import json
import os.path

from common import file, console
from manage import get_excerpt

page_list_file = list()
page_list = list()

def update():
    global page_list, page_list_file
    page_list_file = json.loads(file.read_file("./config/page.json"))
    if len(page_list_file) == 0:
        console.log("Error", "The page list can not be blank.")
        return False
    page_list = page_list_file

    for item in page_list_file:
        processing_file = "./document/{0}.md".format(item["name"])
        file_exists = os.path.exists(processing_file)
        if not file_exists:
            console.log("Remove", "Removing from list: {0}".format(processing_file))
            del page_list[item]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [build_excerpt(item) for item in page_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    file.write_file("./config/page.json", json.dumps(page_list, ensure_ascii=False, indent=4, sort_keys=False))
    console.log("Success", "Update article metadata is successful!")
    return True
@asyncio.coroutine
def async_get_excerpt(file):
    return get_excerpt.get_excerpt(file)

@asyncio.coroutine
def build_excerpt(item):
    global page_list
    processing_file = "./document/{0}.md".format(item["name"])
    console.log("Build", "Processing file: {0}".format(processing_file))
    page_list[page_list.index(item)]["excerpt"] = yield from async_get_excerpt(processing_file)
