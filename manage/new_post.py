import json
import os.path
import re
import time

#from pypinyin import lazy_pinyin
from xpinyin import Pinyin

from common import file, console
from manage import get

system_info = json.loads(file.read_file("./config/system.json"))

def get_name(name_input):
    p = Pinyin()
    name = re.sub('[\/:*?"<>|]', '', name_input)
    name = name.replace(" ", "-")
    return p.get_pinyin(name)

def new_post_init(config, independent=False):
    title = config["title"]
    name = config["name"]

    if not os.path.exists("./document/{0}.md".format(name)):
        editor = system_info["Editor"]
        os.system("{0} ./document/{1}.md".format(editor, name))
    post_info = {"name": name, "title": title, "time": time.time()}

    if not independent and os.path.exists("./document/{0}.md".format(name)):
        excerpt = get.get_excerpt("./document/{0}.md".format(name))
        post_info["excerpt"] = excerpt

    write_json = post_info
    page_config = "./document/{0}.json".format(name)

    if not independent:
        write_json = json.loads(file.read_file("./config/page.json"))
        write_json.insert(0, post_info)
        page_config = "./config/page.json"

    file.write_file(page_config, json.dumps(write_json, indent=4, sort_keys=False, ensure_ascii=False))

    console.log("Success", "Create a new article successfully!")
