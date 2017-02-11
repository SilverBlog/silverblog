#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json

import PyRSS2Gen
import misaka as markdown


class NoOutput:
    def __init__(self):
        pass
    def publish(self, handler):
        pass


class rss_item(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)

    def publish(self, handler):
        self.do_not_autooutput_description = self.description
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        handler._write("<{1}><![CDATA[{0}]]></{1}>".format(self.do_not_autooutput_description, "description"))


def make_rss(project_name, project_url, project_description, page_list):
    page_rss_list = list();
    for item in page_list:
        page_rss_list.append(rss_item(
            title=item["title"],
            link=project_url + "/" + item["name"],
            description=str(markdown.html(ReadDocument("./document/" + item["name"] + ".md"),
                                          extensions=markdown.EXT_FENCED_CODE | markdown.EXT_AUTOLINK | markdown.EXT_TABLES | markdown.EXT_STRIKETHROUGH | markdown.EXT_UNDERLINE)),
            guid=PyRSS2Gen.Guid(project_url + "/" + item["name"]),
            pubDate=item["time"]
        ))
    rss = PyRSS2Gen.RSS2(
        title=project_name,
        link=project_url,
        description=project_description,
        lastBuildDate=datetime.datetime.now(),
        items=page_rss_list)
    return rss.to_xml(encoding='utf-8')
def ReadDocument(filename):
    f = open(filename, newline=None)
    return f.read()


def write_rss(page_list_input):
    system_json_read = open("./config/system.json", newline=None)
    system_config = system_json_read.read()
    system_json_read.close()
    system_config = json.loads(system_config)
    rss = make_rss(system_config["Project_name"], system_config["Project_URL"], system_config["Project_description"],
                   page_list_input)
    write_file = open("./document/rss.xml", "w", newline=None)
    write_file.write(rss)
    write_file.close()


if __name__ == '__main__':
    f = open("./config/page.json", newline=None)
    page_list_raw = f.read()
    f.close()
    page_list = json.loads(page_list_raw)
    write_rss(page_list)
