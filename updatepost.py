import json
import markdown
import filter

f = open("./config/page.json", newline=None)
config=f.read()
f.close()
pagelist = json.loads(config)
for item in pagelist:
    Document = open ("./document/" + item["name"]+".md", newline=None)
    Document=Document.read()
    excerpt=filter.filter_tags(markdown.markdown(Document))[0:140]
    item["excerpt"]=excerpt
f = open("./config/page.json","w", newline=None)
f.write(json.dumps(pagelist))
f.close()