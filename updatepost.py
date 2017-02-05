import json
import misaka as markdown
import filter

f = open("./config/page.json", newline=None)
config = f.read()
f.close()
pagelist = json.loads(config)
for item in pagelist:
    Document = open("./document/" + item["name"] + ".md", newline=None)
    Document = Document.read()
    filetered = filter.filter_tags(markdown.html(Document))
    if len(filetered) > 140:
        excerpt = filetered[0:140]
    else:
        excerpt = filetered
    item["excerpt"] = excerpt
f = open("./config/page.json", "w", newline=None)
f.write(json.dumps(pagelist,ensure_ascii=False))
f.close()
