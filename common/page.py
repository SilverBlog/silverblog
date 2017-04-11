import json
import os.path
import time
from jinja2 import Environment, PackageLoader

from common import file, markdown

env = Environment(loader=PackageLoader('init', 'templates'))


def build_index(page, system_config, page_list, menu_list, static,template_config):
    page_info = {"title": "index"}
    Start_num = -system_config["Paging"] + (int(page) * system_config["Paging"])
    page_row_mod = divmod(len(page_list), system_config["Paging"])
    if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
        page_row = page_row_mod[0] + 1
    else:
        page_row = page_row_mod[0]
    if page_row == 0:
        page_row = 1
    if page <= 0 or page > page_row:
        return None,0
    index_list = page_list[Start_num:Start_num + system_config["Paging"]]
    template = env.get_template("./{0}/index.html".format(system_config["Theme"]))
    result = template.render(menu_list=menu_list,
                             page_list=index_list,
                             page_info=page_info,
                             system_config=system_config,
                             template_config=template_config,
                             page_row=page_row,
                             now_page=page, last_page=page - 1, next_page=page + 1, static=static, now_time=time.localtime())
    return result, page_row


def build_page(name, system_config, page_list, page_name_list, menu_list, static,template_config):
    content = file.read_file("document/{0}.md".format(name))
    page_info = {"title": "undefined"}
    if name in page_name_list:
        page_info = page_list[page_name_list.index(name)]
    if os.path.exists("document/{0}.json".format(name)):
        page_info = json.loads(file.read_file("document/{0}.json".format(name)))
    document = markdown.markdown(content)
    template = env.get_template("./{0}/post.html".format(system_config["Theme"]))
    result = template.render(page_info=page_info, menu_list=menu_list, content=document,
                             system_config=system_config, static=static, template_config=template_config,now_time=time.localtime())
    return result


def build_restful_result(name, system_config, page_list, page_name_list, menu_list):
    content = None
    page_info = None
    if name != "index":
        content = file.read_file("document/{0}.md".format(name))
        page_info = {"title": "undefined"}
        if name in page_name_list:
            page_info = page_list[page_name_list.index(name)]
        if os.path.exists("document/{0}.json".format(name)):
            page_info = json.loads(file.read_file("document/{0}.json".format(name)))
        content = markdown.markdown(content)
    result = {"menu_list": menu_list, "page_list": page_list, "system_config": system_config, "page_info": page_info,
              "content": content}
    return json.dumps(result, ensure_ascii=False)
