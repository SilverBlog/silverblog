#!/usr/bin/env python3
# -*- coding: utf-8 -*
import json
import os.path

import misaka as markdown

import getexcerpt
import genrss

f = open("./config/page.json", newline=None)
page_list_row = f.read()
f.close()
page_list = json.loads(page_list_row)
remove_list = list()
for item in page_list:
    if not os.path.isfile("./document/" + item["name"] + ".md"):
        remove_list.append(item["name"])
    else:
        item["excerpt"] = getexcerpt.get_excerpt("./document/" + item["name"] + ".md")

for item in range(len(page_list) - 1, -1, -1):
    if page_list[item]["name"] in remove_list:
        page_list.pop(item)

f = open("./config/page.json", "w", newline=None)
f.write(json.dumps(page_list, ensure_ascii=False))
f.close()
genrss.write_rss(page_list)
