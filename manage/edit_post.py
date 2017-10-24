import json
import os
import shutil

from common import console, file

def edit(page_list, post_index, config, editor=None, is_menu=False):
    if page_list[post_index]["name"] is not config["name"]:
        shutil.move("./document/{0}.md".format(page_list[post_index]["name"]),
                    "./document/{0}.md".format(config["name"]))
        if os.path.exists("./document/{0}.json".format(page_list[post_index]["name"])):
            shutil.move("./document/{0}.json".format(page_list[post_index]["name"]),
                        "./document/{0}.json".format(config["name"]))
            config_file = json.loads(file.read_file("./document/{0}.json".format(config["name"])))
            config_file["title"] = config["title"]
            file.write_file("./document/{0}.json".format(config["name"]),
                            json.dumps(config_file, indent=4, sort_keys=False, ensure_ascii=False))
        page_list[post_index]["name"] = config["name"]
    if editor is not None:
        os.system("{0} ./document/{1}.md".format(editor, config["name"]))
    page_list[post_index]["title"] = config["title"]
    file_url = "./config/page.json"
    if is_menu:
        file_url = "./config/menu.json"
    file.write_file(file_url, json.dumps(page_list, indent=4, sort_keys=False, ensure_ascii=False))
    console.log("Success", "Edit a new article successfully!")
