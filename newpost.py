import json
from pypinyin import lazy_pinyin
import datetime
import os,os.path
import markdown
import re

def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('', s)
    blank_line_l = re.compile('\n')
    s = blank_line_l.sub('', s)
    blank_kon = re.compile('\t')
    s = blank_kon.sub('', s)
    blank_one = re.compile('\r\n')
    s = blank_one.sub('', s)
    blank_two = re.compile('\r')
    s = blank_two.sub('', s)
    blank_three = re.compile(' ')
    s = blank_three.sub('', s)
    return s

title = input("请输入文章标题: ")
tempname=title.replace(" ","")
tempname=tempname.replace(",","")
tempname=tempname.replace(".","")
tempname=tempname.replace("，","")
tempname=tempname.replace("。","")
tempname=tempname.replace("？","")
tempname=tempname.replace("?","")
tempname=tempname.replace("/","")
tempname=tempname.replace("\\","")
tempname=tempname.replace("(","")
tempname=tempname.replace("（","")
tempname=tempname.replace(")","")
tempname=tempname.replace("）","")
tempname=tempname.replace("!","")
tempname=tempname.replace("！","")
tempname=tempname.replace("-","")
tempname=tempname.replace("——","")
namelist = lazy_pinyin(tempname)
name = ""
for item in namelist:
    name = name + "-" + item
name=name[1:len(name)]
os.system("vim ./document/" + name+".md")
Document = open ("./document/" + name+".md", newline=None)
Document=Document.read()
excerpt=filter_tags(markdown.markdown(Document))[0:140]
postinfo = {"name": name, "title": title, "excerpt": excerpt, "time": str(datetime.date.today())}
if os.path.isfile("./config/page.json"):
    f = open("./config/page.json", newline=None)
    config=f.read()
    f.close()
    pagelist = json.loads(config)
else:
    pagelist=list()
pagelist.insert(0, postinfo)
f = open("./config/page.json","w", newline=None)
f.write(json.dumps(pagelist))
f.close()
