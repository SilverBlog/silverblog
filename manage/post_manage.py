import json
import os
import shutil

from common import file, console
from manage import get

page_list_file = list()
page_list = list()


def new_post(config, independent=False):
    import time
    system_info = json.loads(file.read_file("./config/system.json"))
    title = config["title"]
    name = get.filter_name(config["name"])
    if not os.path.exists("./document/{}.md".format(name)):
        editor = system_info["Editor"]
        os.system("{0} ./document/{1}.md".format(editor, name))
    post_info = {"name": name, "title": title, "time": time.time()}
    if not os.path.exists("./document/{}.md".format(name)):
        console.log("Error", "Cannot find [./document/{}.md]".format(name))
        return
    if not independent:
        excerpt = get.get_excerpt("./document/{}.md".format(name))
        post_info["excerpt"] = excerpt

    write_json = post_info
    page_config = "./document/{}.json".format(name)

    if not independent:
        write_json = json.loads(file.read_file("./config/page.json"))
        write_json.insert(0, post_info)
        page_config = "./config/page.json"

    file.write_file(page_config, file.json_format_dump(write_json))

    console.log("Success", "Create a new article successfully!")


def edit_post(page_list, post_index, config, editor=None, is_menu=False):
    if page_list[post_index]["name"] is not config["name"]:
        safe_name = get.filter_name(config["name"])
        shutil.move("./document/{}.md".format(page_list[post_index]["name"]),
                    "./document/{}.md".format(safe_name))
        if os.path.exists("./document/{}.json".format(page_list[post_index]["name"])):
            shutil.move("./document/{}.json".format(page_list[post_index]["name"]),
                        "./document/{}.json".format(safe_name))
            config_file = json.loads(file.read_file("./document/{}.json".format(safe_name)))
            config_file["title"] = config["title"]
            file.write_file("./document/{}.json".format(safe_name),
                            file.json_format_dump(config_file))
        page_list[post_index]["name"] = safe_name
    if editor is not None:
        os.system("{0} ./document/{1}.md".format(editor, safe_name))
    page_list[post_index]["title"] = config["title"]
    file_url = "./config/page.json"
    if is_menu:
        file_url = "./config/menu.json"
    file.write_file(file_url, file.json_format_dump(page_list))
    console.log("Success", "Edit a new article successfully!")


def delete_post(page_list, post_index):
    file_name = page_list[post_index]["name"]
    meta_backup = page_list[post_index]
    del page_list[post_index]
    file.write_file("./config/page.json", file.json_format_dump(page_list))
    if not os.path.exists("./trash"):
        os.mkdir("./trash")
    check_file("{}.md".format(file_name))
    check_file("{}.json".format(file_name))
    file.write_file("./trash/{}.json".format(file_name), file.json_format_dump(meta_backup))
    shutil.move("./document/{}.md".format(file_name), "./trash/{}.md".format(file_name))


def check_file(file_name):
    if os.path.exists("./trash/{}".format(file_name)):
        os.remove("./trash/{}".format(file_name))


def update_post():
    import asyncio
    global page_list, page_list_file
    page_list_file = json.loads(file.read_file("./config/page.json"))
    if len(page_list_file) == 0:
        console.log("Error", "The page list can not be blank.")
        return False
    page_list = page_list_file

    for item in page_list_file:
        processing_file = "./document/{}.md".format(item["name"])
        file_exists = os.path.exists(processing_file)
        if not file_exists:
            console.log("Remove", "Removing from list: {}".format(processing_file))
            del page_list[item]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [build_excerpt(item) for item in page_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    file.write_file("./config/page.json", file.json_format_dump(page_list))
    console.log("Success", "Update article metadata is successful!")
    return True


@asyncio.coroutine
def async_get_excerpt(file_name):
    return get.get_excerpt(file_name)


@asyncio.coroutine
def build_excerpt(item):
    global page_list
    processing_file = "./document/{}.md".format(item["name"])
    console.log("Build", "Processing file: {}".format(processing_file))
    custom_config_file = "./document/{}.json".format(item["name"])
    if os.path.exists(custom_config_file):
        console.log("Build", "Processing file: {}".format(custom_config_file))
        custom_config_content = yield from file.async_read_file(custom_config_file)
        custom_config = json.loads(custom_config_content)
        page_list[page_list.index(item)].update(custom_config)
        if "excerpt" in custom_config:
            return
    page_list[page_list.index(item)]["excerpt"] = yield from async_get_excerpt(processing_file)
