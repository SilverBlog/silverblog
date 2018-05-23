import json
import os
import shutil

from common import console, file
from manage import get


def edit(page_list, post_index, config, editor=None, is_menu=False):
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
