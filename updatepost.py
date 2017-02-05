import json
import os.path

import misaka as markdown

import filter

f = open("./config/page.json", newline=None)
pagelist_row = f.read()
f.close()
pagelist = json.loads(pagelist_row)
removelist = list()
for item in pagelist:
    if not os.path.isfile("./document/" + item["name"] + ".md"):
        removelist.append(item["name"])
    else:
        Document = open("./document/" + item["name"] + ".md", newline=None)
        Document = Document.read()
        filetered = filter.filter_tags(markdown.html(Document))
        if len(filetered) > 140:
            excerpt = filetered[0:140]
        else:
            excerpt = filetered
        item["excerpt"] = excerpt

for item in range(len(pagelist) - 1, -1, -1):
    if pagelist[item]["name"] in removelist:
        pagelist.pop(item)

f = open("./config/page.json", "w", newline=None)
f.write(json.dumps(pagelist,ensure_ascii=False))
f.close()
