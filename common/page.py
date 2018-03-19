import json
import os.path
import time

from jinja2 import Environment, PackageLoader

from common import file, markdown, post_map

env = Environment(loader=PackageLoader('init', 'templates'))

def format_datetime(value, format='%Y-%m-%d %H:%M'):
    return str(time.strftime(format, value))

def get_i18n_value(i18n, value):
    if value in i18n:
        return i18n[value]
    return value

env.filters["get_i18n_value"] = get_i18n_value
env.filters['format_datetime'] = format_datetime
#Obsolete
env.filters['datetimeformat'] = format_datetime

def build_index(page, system_config, page_list, menu_list, template_config, i18n=None):
    page_info = {"title": "index"}
    paging = system_config["Paging"]
    start_num = -paging + (int(page) * paging)
    page_row_mod = divmod(len(page_list), system_config["Paging"])
    page_row = page_row_mod[0]
    if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
        page_row = page_row_mod[0] + 1
    if page_row == 0:
        page_row = 1
    if page <= 0 or page > page_row:
        return None, 0
    index_list = page_list[start_num:start_num + paging]
    template = env.get_template("./{0}/index.html".format(system_config["Theme"]))
    result = template.render(menu_list=menu_list,
                             page_list=index_list,
                             page_info=page_info,
                             system_config=system_config,
                             template_config=template_config,
                             page_row=page_row,
                             now_page=page, now_time=time.localtime(), i18n=i18n)
    return result, page_row

def build_page(name, system_config, page_info, menu_list, template_config, i18n=None):
    content = file.read_file("./document/{0}.md".format(name))
    if page_info is None:
        page_info = {"title": "undefined"}
    if os.path.exists("./document/{0}.json".format(name)):
        page_info = json.loads(file.read_file("document/{0}.json".format(name)))
        if "time" in page_info:
            page_info["time"] = str(post_map.build_time(page_info["time"], system_config))
    document = markdown.markdown(content)
    template = env.get_template("./{0}/post.html".format(system_config["Theme"]))
    result = template.render(page_info=page_info, menu_list=menu_list, content=document,
                             system_config=system_config, template_config=template_config,
                             now_time=time.localtime(), i18n=i18n)
    return result
