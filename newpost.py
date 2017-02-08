#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os.path
import sys
import misaka as markdown
import filter
from pypinyin import lazy_pinyin

def getname(nameinput):
    if len(nameinput) == 0:
        tempname = title.replace(" ", "").replace(",", "").replace(".", "").replace("，", "").replace("。", "").replace(
            "？",
            "").replace(
            "?", "").replace("/", "").replace("/", "").replace("\\", "").replace("(", "").replace("（", "").replace(")",
                                                                                                                   "").replace(
            "）", "").replace("!", "").replace("！", "").replace("——", "")
        namelist = lazy_pinyin(tempname)
        name = ""
        for item in namelist:
            name = name + "-" + item
        return name[1:len(name)]
    else:
        return nameinput

if len(sys.argv)>1:
    if os.path.isfile(sys.argv[1]):
        config = open(sys.argv[1], newline=None)
        config = json.loads(config.read())
        title=config["title"]
        name=config["name"]
        file=config["file"]
    else:
        print("找不到文件！")
        exit()
else:
    title = input("请输入文章标题: ")
    name = input("请输入文章URL(留空使用标题拼音):")
    file = input("请输入要复制的文件路径(留空或不存在将新建):")
name=getname(name)
if os.path.isfile(file):
    os.system("cp " + file + " ./document/" + name + ".md")
else:
    os.system("vim ./document/" + name + ".md")
Document = open("./document/" + name + ".md", newline=None)
Document = Document.read()
filetered = filter.filter_tags(markdown.html(Document))
if len(filetered) > 140:
    excerpt = filetered[0:140]
else:
    excerpt = filetered
postinfo = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
if os.path.isfile("./config/page.json"):
    f = open("./config/page.json", newline=None)
    pagelist_raw = f.read()
    f.close()
    pagelist = json.loads(pagelist_raw)
else:
    pagelist = list()
pagelist.insert(0, postinfo)
f = open("./config/page.json", "w", newline=None)
f.write(json.dumps(pagelist,ensure_ascii=False))
f.close()

