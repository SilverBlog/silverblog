import json
import os
import uuid

from common import file


def add_menu(menu_info):
    menu_item = dict()
    menu_item["title"] = menu_info["title"]
    if menu_info["type"]:
        menu_item["name"] = menu_info["name"]
        menu_item["uuid"] = str(uuid.uuid5(uuid.NAMESPACE_URL, menu_info["name"]))
    if not menu_info["type"]:
        menu_item["absolute"] = menu_info["name"]
    menu_file = json.loads(file.read_file("./config/menu.json"))
    menu_file.append(menu_item)
    file.write_file("./config/menu.json", file.json_format_dump(menu_file))


def edit_menu(menu_list, menu_index, menu_info):
    menu_item = dict()
    menu_item["title"] = menu_info["title"]
    if menu_info["type"]:
        menu_item["name"] = menu_info["name"]
        menu_item["uuid"] = str(uuid.uuid5(uuid.NAMESPACE_URL, menu_info["name"]))
    if not menu_info["type"]:
        menu_item["absolute"] = menu_info["name"]
    menu_list[menu_index] = menu_item

    if menu_info["type"] and menu_info["editor"] is not None:
        os.system("{0} ./document/{1}.md".format(menu_info["editor"], menu_item["name"]))
    file.write_file("./config/menu.json", file.json_format_dump(menu_list))


def delete_menu(menu_list, select_index):
    del menu_list[select_index]
    file.write_file("./config/menu.json", file.json_format_dump(menu_list))
