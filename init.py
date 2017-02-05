import datetime
import json
import os
import os.path
import misaka as markdown
import PyRSS2Gen
import redis
from flask import Flask, abort, render_template

app = Flask(__name__)


# 分组页面
@app.route("/")
@app.route("/<pagename>")
@app.route("/<pagename>/")
@app.route('/<pagename>/page:<page>')
@app.route('/<pagename>/page:<page>/')
def LoadPage(pagename="index", page="1"):
    cache_pagename = pagename
    cache_result = GetCache(cache_pagename + "/page:" + str(page))
    if cache_result is not None:
        return cache_result
    if pagename == "index":
        return LoadIndex(int(page))
    if pagename == "rss" or pagename == "feed":
        return pagerss, 200, {'Content-Type': 'text/xml; charset=utf-8'}
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
    Document = render_template("index.html", title="主页", menu_list=menu_list, page_list=pagelist,
                               project_name=project_name, project_description=project_description,
                               pagerow=page_row - 1, author_image=author_image, cover_image=system_info["Cover_image"],
                               nowpage=page, lastpage=page - 1, newpage=page + 1)
    SetCache("index/page:" + str(page), Document)
    return Document


def LoadDocument(name):
    request_page = name
    Document_Raw = ReadDocument("document/" + name + ".md")
    if name in page_name_list:
        pageinfo = page_list[page_name_list.index(name)]
        Document = Document_Raw
    else:
        Documents = Document_Raw.split("<!--infoend-->")
        pageinfo = json.loads(Documents[0])
        Document = Documents[1]
    Document=markdown.html(Document,extensions=markdown.EXT_NO_INTRA_EMPHASIS | markdown.EXT_FENCED_CODE |
            markdown.EXT_AUTOLINK | markdown.EXT_LAX_HTML_BLOCKS |
            markdown.EXT_TABLES)
    Document = render_template("post.html", title=pageinfo["title"], pageinfo=pageinfo, menu_list=menu_list,
                               project_name=project_name, context=Document, author_image=author_image,
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


def genrss():
    pagersslist = list();
    for item in page_list:
        pagersslist.append(PyRSS2Gen.RSSItem(
            title=item["title"],
            link="/" + item["name"],
            description=item["excerpt"],
            guid=PyRSS2Gen.Guid(project_url + "/" + item["name"]),
            pubDate=item["time"]))

    rss = PyRSS2Gen.RSS2(
        title=project_name,
        link=project_url,
        description=project_description,
        lastBuildDate=datetime.datetime.now(),
        items=pagersslist)
    return rss.to_xml(encoding='utf-8')


page_list = json.loads(ReadDocument("config/page.json"))
menu_list = json.loads(ReadDocument("config/menu.json"))
system_info = json.loads(ReadDocument("config/system.json"))
project_name = system_info["Project_name"]
project_url = system_info["Project_URL"]
project_description = system_info["Project_description"]
author_image = system_info["author_image"]
Item_name_list = getItemName()
page_name_list = list()
pagerss = genrss()
for item in page_list:
    page_name_list.append(item["name"])
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
