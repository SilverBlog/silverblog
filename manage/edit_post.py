import os
import shutil

from common import console, file

def edit(page_list, post_index, config, editor=None):
    if page_list[post_index]["name"] is not config["name"]:
        shutil.move("./document/{0}.md".format(page_list[post_index]["name"]),
                    "./document/{0}.md".format(config["name"]))
        page_list[post_index]["name"] = config["name"]
    if editor is not None:
        os.system("{0} ./document/{1}.md".format(editor, config["name"]))
    page_list[post_index]["title"] = config["title"]
    file.write_file("./config/page.json", json.dumps(page_list, indent=4, sort_keys=False, ensure_ascii=False))
    console.log("Success", "Edit a new article successfully!")
