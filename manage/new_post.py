import datetime
import json
import os.path
import re
import shutil

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


def new_post_init(config, editor,independent=False):
    if config is not None:
        config = json.loads(config)
        title = config["title"]
        name = config["name"]
        filename = config["file"]
    else:
        title = input("Please enter the title of the article:")
        name = input("Please enter the URL (Leave a blank use pinyin):")
        filename = None

    if len(name) == 0:
        name = get_name(title)

    if filename is not None and os.path.exists(filename):
        shutil.copyfile(filename, "./document/{0}.md".format(name))

    if config is None:
        # Check if the editor configuration exists
        if editor is None:
            editor = "vim"
            if "Editor" in system_info:
                editor = system_info["Editor"]
        os.system("{0} ./document/{1}.md".format(editor, name))
    excerpt = get_excerpt.get_excerpt("./document/{0}.md".format(name))
    post_info = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
    write_json=post_info
    page_config="./document/{0}.json".format(name)
    if not independent:
        write_json = json.loads(file.read_file("./config/page.json"))
        write_json.insert(0, post_info)
        page_config="./config/page.json"

    file.write_file(page_config, json.dumps(write_json, ensure_ascii=False))
    console.log("Success","Create a new article successfully!","green")
