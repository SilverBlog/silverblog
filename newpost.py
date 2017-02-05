import datetime
import json
import os.path
import misaka as markdown
from pypinyin import lazy_pinyin

title = input("请输入文章标题: ")
nameinput = input("请输入文章URL(留空使用标题拼音):")
if len(nameinput) == 0:
    tempname = title.replace(" ", "").replace(",", "").replace(".", "").replace("，", "").replace("。", "").replace("？",
                                                                                                                  "").replace(
        "?", "").replace("/", "").replace("/", "").replace("\\", "").replace("(", "").replace("（", "").replace(")",
                                                                                                               "").replace(
        "）", "").replace("!", "").replace("！", "").replace("——", "")
    namelist = lazy_pinyin(tempname)
    name = ""
    for item in namelist:
        name = name + "-" + item
    name = name[1:len(name)]
else:
    name = nameinput
file = input("请输入要复制的文件路径(留空或不存在将新建):")
if len(nameinput) != 0:
    os.system("cp " + file + " ./document/" + name + ".md")
os.system("vim ./document/" + name + ".md")
Document = open("./document/" + name + ".md", newline=None)
Document = Document.read()
filetered = filter.filter_tags(markdown.html(Document))
if len(filetered) > 140:
    excerpt = filetered[0:140]
else:
    excerpt = filetered
postinfo = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
if os.path.isfile("./config/page.json"):
    f = open("./config/page.json", newline=None)
    config = f.read()
    f.close()
    pagelist = json.loads(config)
else:
    pagelist = list()
pagelist.insert(0, postinfo)
f = open("./config/page.json", "w", newline=None)
f.write(json.dumps(pagelist,ensure_ascii=False))
f.close()
