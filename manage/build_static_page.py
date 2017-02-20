import json
import os
import shutil

from jinja2 import Environment, PackageLoader

from common import file
from common import markdown

env = Environment(loader=PackageLoader('init', 'templates'))


def build_index(page, menu_list, page_list, system_config):
    page_info = {"title": "主页"}
    Start_num = -system_config["Paging"] + (int(page) * system_config["Paging"])
    page_row_mod = divmod(len(page_list), system_config["Paging"])
    if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
        page_row = page_row_mod[0] + 2
    else:
        page_row = page_row_mod[0] + 1
    index_list = page_list[Start_num:Start_num + system_config["Paging"]]
    template = env.get_template("./{0}/index.html".format(system_config["Theme"]))
    content = template.render(menu_list=menu_list,
                              page_list=index_list,
                              page_info=page_info,
                              system_config=system_config,
                              page_row=page_row - 1,
                              now_page=page, last_page=page - 1, next_page=page + 1, static=True)
    return content, page_row


def build_page(name, menu_list, page_list, system_config, page_name_list):
    Document_Raw = file.read_file("./document/{0}.md".format(name))
    if name in page_name_list:
        page_info = page_list[page_name_list.index(name)]
        content = Document_Raw
    else:
        Documents = Document_Raw.split("<!--infoend-->")
        page_info = json.loads(Documents[0])
        content = Documents[1]
    document = markdown.markdown(content)
    template = env.get_template("./{0}/post.html".format(system_config["Theme"]))
    content = template.render(page_info=page_info, menu_list=menu_list, content=document,
                              system_config=system_config, static=True)
    return content


def build():
    page_list = json.loads(file.read_file("./config/page.json"))
    menu_list = json.loads(file.read_file("./config/menu.json"))
    system_config = json.loads(file.read_file("./config/system.json"))
    page_name_list = list()
    for item in page_list:
        page_name_list.append(item["name"])
    content, row = build_index(1, menu_list, page_list, system_config)
    file.write_file("./static_page/index.html", content)
    file.write_file("./static_page/index_1.html", content)
    if row != 0:
        for page_id in range(2, row):
            content, row = build_index(page_id, menu_list, page_list, system_config)
            file.write_file("./static_page/index_{0}.html".format(str(page_id)), content)
    for filename in os.listdir("./document/"):
        if filename.endswith(".md"):
            file.write_file("./static_page/{0}.html".format(filename.replace(".md", "")),
                            build_page(filename.replace(".md", ""), menu_list, page_list, system_config,
                                       page_name_list))
    shutil.copytree("./templates/static/{0}/".format(system_config["Theme"]),
                    "./static_page/static/{0}/".format(system_config["Theme"]))
    shutil.copytree("./templates/static/user_file",
                    "./static_page/static/user_file")
    shutil.copyfile("./document/rss.xml","./static_page/rss.xml")
