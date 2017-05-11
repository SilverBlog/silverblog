import json
import os.path
import re
import time

from pypinyin import lazy_pinyin

from common import file, console
from manage import get_excerpt

system_info = json.loads(file.read_file("./config/system.json"))


def get_name(nameinput):
    name_raw = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", nameinput)
    namelist = lazy_pinyin(name_raw)
    name = ""
    for item in namelist:
        name = name + "-" + item
    return name[1:len(name)]


def new_post_init(config, independent=False):
    if config is not None:
        title = config["title"]
        name = config["name"]
    else:
        print("Please enter the title of the article:")
        title = input()
        print("Please enter the URL (Leave a blank use pinyin):")
        name = input()

    if len(name) == 0:
        name = get_name(title)

    if config is None:
        editor = system_info["Editor"]
        os.system("{0} ./document/{1}.md".format(editor, name))
    post_info = {"name": name, "title": title, "time": str(time.strftime(system_info["Time_Format"], time.localtime()))}

    if not independent:
        excerpt = get_excerpt.get_excerpt("./document/{0}.md".format(name))
        post_info["excerpt"] = excerpt

    write_json = post_info
    page_config = "./document/{0}.json".format(name)

    if not independent:
        write_json = json.loads(file.read_file("./config/page.json"))
        write_json.insert(0, post_info)
        page_config = "./config/page.json"

    file.write_file(page_config, json.dumps(write_json, ensure_ascii = False))

    console.log("Success","Create a new article successfully!")
