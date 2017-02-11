import PyRSS2Gen
import datetime
import misaka as markdown
import json
class NoOutput:
    def __init__(self):
        pass
    def publish(self, handler):
        pass

class IPhoneRSS2(PyRSS2Gen.RSSItem):
    def __init__(self, **kwargs):
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)

    def publish(self, handler):
        self.do_not_autooutput_description = self.description
        self.description = NoOutput()
        PyRSS2Gen.RSSItem.publish(self, handler)

    def publish_extensions(self, handler):
        handler._write('<%s><![CDATA[%s]]></%s>' % ("description", self.do_not_autooutput_description, "description"))

def makerss(project_name,project_url,project_description,page_list):
    pagersslist = list();
    for item in page_list:
        pagersslist.append(IPhoneRSS2(
            title=item["title"],
            link=project_url + "/" + item["name"],
            description=str(markdown.html(ReadDocument("./document/"+item["name"]+".md"))),
            guid=PyRSS2Gen.Guid(project_url + "/" + item["name"]),
            pubDate=item["time"]
        ))
    rss = PyRSS2Gen.RSS2(
        title=project_name,
        link=project_url,
        description=project_description,
        lastBuildDate=datetime.datetime.now(),
        items=pagersslist)
    return rss.to_xml(encoding='utf-8')
def ReadDocument(filename):
    f = open(filename, newline=None)
    return f.read()
def writerss(pagelist):
    f = open("./config/system.json", newline=None)
    config = f.read()
    f.close()
    config = json.loads(config)
    rss = makerss(config["Project_name"], config["Project_URL"], config["Project_description"], pagelist)
    f = open("./document/rss.xml", "w", newline=None)
    f.write(rss)
    f.close()
if __name__ == '__main__':
    f = open("./config/page.json", newline=None)
    pagelist_raw = f.read()
    f.close()
    pagelist = json.loads(pagelist_raw)
    writerss(pagelist)