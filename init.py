import json
import os, os.path
import markdown
import redis
from flask import Flask, abort, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', systemtitle=system_title), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html', systemtitle=system_title), 500


# 分组页面
@app.route("/")
@app.route("/<pagename>")
@app.route('/<pagename>/page:<page>')
def LoadPage(pagename="index", page="1"):
    cache_pagename = pagename
    cache_result = GetCache(cache_pagename + "/page:" + str(page))
    if cache_result is not None:
        return cache_result
    if pagename == "index":
        LoadIndex(int(page))
    if os.path.isfile("document/" + pagename + ".md"):
        return LoadDocument(pagename)
    else:
        abort(404)


def LoadIndex(page):
    Start_num = -system_info["Paging"] + (int(page) * system_info["Paging"])
    page_row_mod = divmod(len(page_list), system_info["Paging"])
    if page_row_mod[1] != 0 and len(page_list) > system_info["Paging"]:
        page_row = page_row_mod[0] + 2
    else:
        page_row = page_row_mod[0] + 1
    if page <= 0:
        abort(404)
    pagelist = page_list[Start_num:Start_num + system_info["Paging"]]
    Document = render_template("index.html", title="主页", menu_list=menu_list, pagelist=pagelist,
                               project_name=project_name, project_description=project_description,
                               pagerow=page_row,
                               nowpage=page, lastpage=page - 1, newpage=page + 1)
    SetCache("index/page:" + str(page), Document)
    return Document


def LoadDocument(name):
    request_page = name
    Document_Raw = ReadDocument("document/" + name + ".md")
    Document = markdown.markdown(Document_Raw)
    pageinfo = page_list[name]
    Document = render_template("post.html", pageinfo=pageinfo, menu_list=menu_list,
                               project_name=project_name, context=Document,
                               requestpage=request_page)
    SetCache(name, Document)
    return Document


def GetCache(pagename):
    if system_info["cache"]:
        try:
            return redis_connect[pagename]
        except:
            return None


def SetCache(pagename, Document):
    if system_info["cache"]:
        redis_connect[pagename] = Document


def ReadDocument(filename):
    f = open(filename, newline=None)
    return f.read()


def getItemName():
    list = []
    for item in page_list:
        list.append(item["name"])
    return list


page_list = json.loads(ReadDocument("config/page.json"))
menu_list = json.loads(ReadDocument("config/menu.json"))
system_info = json.loads(ReadDocument("config/system.json"))
project_name = system_info["Project_name"]
project_description=system_info["project_description"]
Item_name_list = getItemName()
if system_info["cache"]:
    if "redis_password" in system_info:
        redis_connect = redis.Redis(host=system_info["redis_connect"], port=6379, db=0,
                                    password=system_info["redis_password"])
    else:
        redis_connect = redis.Redis(host=system_info["redis_connect"], port=6379, db=0)
    redis_connect.flushdb()
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
