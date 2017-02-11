#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import os.path
import sys

from pypinyin import lazy_pinyin

import getexcerpt
import genrss


def getname(nameinput):
        tempname = nameinput.replace(" ", "").replace(",", "").replace(".", "").replace("，", "").replace("。", "").replace(
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

def new_post(name,title,file,content=""):
    if len(name)==0:
        name=title
    name=getname(name)
    if len(content)!=0:
        Document = open("./document/" + name + ".md","w", newline=None)
        Document.write(content)
        Document.close()
    else:
        if os.path.isfile(file):
            os.system("cp " + file + " ./document/" + name + ".md")
        else:
            os.system("vim ./document/" + name + ".md")
    excerpt = getexcerpt.get_excerpt("./document/" + name + ".md")
    postinfo = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
    if os.path.isfile("./config/page.json"):
        f = open("./config/page.json", newline=None)
        pagelist_raw = f.read()
        f.close()
        page_list = json.loads(pagelist_raw)
    else:
        page_list = list()
    page_list.insert(0, postinfo)
    f = open("./config/page.json", "w", newline=None)
    f.write(json.dumps(page_list, ensure_ascii=False))
    f.close()
    genrss.write_rss(page_list)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            config = open(sys.argv[1], newline=None)
            config = json.loads(config.read())
            title = config["title"]
            name = config["name"]
            file = config["file"]
        else:
            print("找不到文件！")
            exit()
    else:
        title = input("请输入文章标题: ")
        name = input("请输入文章URL(留空使用标题拼音):")
        file = input("请输入要复制的文件路径(留空或不存在将新建):")
    new_post(name,title,file)