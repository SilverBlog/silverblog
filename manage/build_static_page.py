import json

from jinja2 import Environment, PackageLoader

from common import file

env = Environment(loader=PackageLoader('SmartBlog', 'templates'))


def build_index(page):
    page_info = {"title": "主页"}
    Start_num = -system_config["Paging"] + (int(page) * system_config["Paging"])
    page_row_mod = divmod(len(page_list), system_config["Paging"])
    if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
        page_row = page_row_mod[0] + 2
    else:
        page_row = page_row_mod[0] + 1
    index_list = page_list[Start_num:Start_num + system_config["Paging"]]
    template = env.get_template("./{0}/index.html".format(system_config["Theme"]))
    template.render(menu_list=menu_list,
                    page_list=index_list,
                    page_info=page_info,
                    system_config=system_config,
                    page_row=page_row - 1,
                    now_page=page, last_page=page - 1, next_page=page + 1)


#def build():


def get_item_name():
    item_list = []
    for page_item in page_list:
        item_list.append(page_item["name"])
    return item_list


page_list = json.loads(file.read_file("config/page.json"))
menu_list = json.loads(file.read_file("config/menu.json"))
system_config = json.loads(file.read_file("config/system.json"))
item_name_list = get_item_name()
page_name_list = list()
for item in page_list:
    page_name_list.append(item["name"])
