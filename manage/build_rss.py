import datetime
import json

import PyRSS2Gen

from common import file
from common import markdown


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
        location = "{0}/{1}".format(item["Project_URL"], item["name"])
        page_rss_list.append(rss_item(
            title=item["title"],
            link=location,
            description=str(markdown.markdown(file.read_file("./document/{0}.md".format(item["name"])))),
            guid=PyRSS2Gen.Guid(location),
            pubDate=item["time"]
        ))
    rss = PyRSS2Gen.RSS2(
        title=project_name,
        link=project_url,
        description=project_description,
        lastBuildDate=datetime.datetime.now(),
        items=page_rss_list)
    return rss.to_xml(encoding='utf-8')


def build_rss():
    page_list = json.loads(file.read_file("./config/page.json"))
    system_config = json.loads(file.read_file("./config/system.json"))
    file.write_file("./document/rss.xml", make_rss(system_config["Project_Name"], system_config["Project_URL"],
                                                   system_config["Project_Description"],
                                                   page_list))
