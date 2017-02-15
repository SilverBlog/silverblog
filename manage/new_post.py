import datetime
import json
import os.path
import re
import shutil

from pypinyin import lazy_pinyin

from common import file
from manage import get_excerpt


def get_name(nameinput):
    name_raw = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", nameinput)
    namelist = lazy_pinyin(name_raw)
    name = ""
    for item in namelist:
        name = name + "-" + item
    return name[1:len(name)]


def new_post(name, title, filename, editor):
    if len(name)==0:
        name = get_name(title)
    if os.path.isfile(filename):
        shutil.copyfile(filename,"./document/{0}.md".format(name))
    else:
        if editor is not None:
            os.system("{0} ./document/{1}.md".format(editor, name))
    excerpt = get_excerpt.get_excerpt("./document/{0}.md".format(name))
    post_info = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
    if os.path.isfile("./config/page.json"):
        page_list = json.loads(file.read_file("./config/page.json"))
    else:
        page_list = list()
    page_list.insert(0, post_info)
    file.write_file("./config/page.json", json.dumps(page_list, ensure_ascii=False))


def new_post_init(config_file=None, editor="vim"):
    if config_file is not None:
        if os.path.isfile(config_file):
            config = json.loads(file.read_file(config_file))
            title = config["title"]
            name = config["name"]
            filename = config["file"]
            new_post(name, title, filename, editor)
    else:
        title = input("请输入文章标题: ")
        name = input("请输入文章URL(留空使用标题拼音):")
        filename = input("请输入要复制的文件路径(留空或不存在将新建):")
        new_post(name, title, filename, editor)
