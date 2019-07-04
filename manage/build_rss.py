import asyncio
import datetime
import json

import PyRSS2Gen

from common import file, markdown, console

rss_item_list = list()


class NoOutput:
    def __init__(self):
        pass

    def publish(self, handler):
        pass


class rss_item(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)
        self.do_not_autooutput_description = self.description

    def publish(self, handler):
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        handler._write("<{1}><![CDATA[{0}]]></{1}>".format(self.do_not_autooutput_description, "description"))


@asyncio.coroutine
def async_markdown(system_config, raw):
    return markdown.markdown(system_config, raw)


@asyncio.coroutine
def make_rss_item(system_config, page_list, item, project_url):
    global rss_item_list
    location = "{0}/post/{1}".format(project_url, item["name"])
    raw_document = yield from file.async_read_file("./document/{0}.md".format(item["name"]))
    desc = yield from async_markdown(system_config, raw_document)
    rss_item_list[page_list.index(item)] = rss_item(title=item["title"], link=location, description=desc,
                                                    guid=PyRSS2Gen.Guid(location),
                                                    pubDate=datetime.datetime.fromtimestamp(item["time"]))


def make_rss(project_name, project_url, project_description, page_list, system_config):
    global rss_item_list
    if len(page_list) != 0:
        rss_item_list = list(range(0, len(page_list)))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [make_rss_item(system_config, page_list, item, system_config["Project_URL"]) for item in page_list]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
    rss = PyRSS2Gen.RSS2(
        title=project_name,
        link=project_url,
        description=project_description,
        lastBuildDate=datetime.datetime.now(),
        items=rss_item_list,
        generator="SilverBlog",
        docs="https://silverblog.org")
    return rss.to_xml(encoding='utf-8')


def build_rss():
    system_config = json.loads(file.read_file("./config/system.json"))
    system_config["Lazyload"] = False
    page_list = json.loads(file.read_file("./config/page.json"))
    file.write_file("./document/rss.xml", make_rss(system_config["Project_Name"], system_config["Project_URL"],
                                                   system_config["Project_Description"],
                                                   page_list, system_config))
    console.log("Success", "Build rss success!")
