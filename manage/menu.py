#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import time

from common import file, console
from manage import whiptail, upgrade, get

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.backtitle = "SilverBlog management tool"
if os.path.exists("./config/system.json"):
    system_config = json.loads(file.read_file("./config/system.json"))
def use_whiptail_mode():
    menu_list = ["Article manager", "Menu manager", "Build static page", "Setting", "=" * 25, "Exit"]
    if upgrade.check_is_git():
        menu_list = ["Article manager", "Menu manager", "Build static page", "Upgrade", "Setting",
                     "=" * 25, "Exit"]
    while True:
        dialog.title = "Home"
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Article manager":
            article_manager()
        if result == "Menu manager":
            menu_manager()
        if result == "Upgrade":
            upgrade_system()
        if result == "Build static page":
            from manage import build_static_page
            dialog.title = "Build static page"
            build_static_page.publish()
            time.sleep(0.5)
        if result == "Setting":
            from manage import setting
            setting.setting_menu()


def article_manager():
    from manage import build_rss, post_manage
    while True:
        dialog.title = "Article manager"
        menu_list = ["New", "Update", "Edit", "Delete", "=" * 25, "Back", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "New":
            dialog.title = "New post"
            post_info = get_post_info()
            if os.path.exists("./document/{}.md".format(post_info["name"])):
                console.log("Error", "File [./document/{}.md] already exists".format(post_info["name"]))
                exit(1)
            if post_info["name"] is not None:
                post_manage.new_post(post_info, dialog.confirm("Is this an independent page?", "no"))
        if result == "Edit":
            dialog.title = "Edit post"
            page_list, post_index = select_list("./config/page.json")
            if page_list:
                config = get_post_info(page_list[post_index]["title"], page_list[post_index]["name"],
                                       page_list[post_index]["time"])
                system_info = json.loads(file.read_file("./config/system.json"))
                post_manage.edit_post(page_list, post_index, config, system_info["Editor"])
            post_manage.update_post()
        if result == "Delete":
            page_list, post_index = select_list("./config/page.json")
            if page_list and dialog.confirm("Are you sure you want to delete this article?", "no"):
                post_manage.delete_post(page_list, post_index)
        if result == "Update":
            post_manage.update_post()
        build_rss.build_rss()
        time.sleep(0.5)

def menu_manager():
    while True:
        dialog.title = "Menu manager"
        menu_list = ["New", "Edit", "Delete", "=" * 25, "Back", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        from manage import menu_manage
        if result == "New":
            menu_info = get_menu_info()
            menu_manage.add_menu(menu_info)
        if result == "Edit":
            menu_list, menu_index = select_list("./config/menu.json")
            if menu_list:
                address=None
                independent=False
                menu_item = menu_list[menu_index]
                if "name" in menu_item:
                    address = menu_item["name"]
                    independent = True
                if "absolute" in menu_item:
                    address = menu_item["absolute"]
                    independent = False
                menu_info = get_menu_info(menu_item["title"], address, independent)
                menu_info["editor"] = system_config["Editor"]
                menu_manage.edit_menu(menu_list, menu_index, menu_info)
        if result == "Delete":
            menu_list, select_index = select_list("./config/menu.json")
            if menu_list and dialog.confirm("Are you sure you want to delete this item?", "no"):
                menu_manage.delete_menu(menu_list, select_index)
        time.sleep(0.5)


def get_menu_info(title_input="", name_input="", independent=False):
    title = dialog.prompt("Please enter the title of the menu:", title_input).strip()
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return {"title": None, "name": None, "type": False}
    is_independent = "no"
    if independent:
        is_independent = "yes"
    is_independent_type = dialog.confirm("Is this an independent page?", is_independent)
    name = None
    if is_independent_type:
        name = dialog.prompt("Please enter the page name:", name_input).strip()
    if not is_independent_type:
        ext_link = dialog.confirm("Is this an external link?")
        if ext_link:
            if name_input == "":
                name_input = "https://"
            name = dialog.prompt("Please enter the address:", name_input).strip()
        if not ext_link:
            page_list, page_index = select_list("./config/page.json")
            name = page_list[page_index]["name"]
    if len(name) == 0:
        dialog.alert("The name can not be blank.")
        return {"title": None, "name": None, "type": False}
    return {"title": title, "name": name, "type": is_independent_type}

def upgrade_system():
    from manage import upgrade
    dialog.title = "Upgrade"
    upgrade_check = upgrade.upgrade_check()
    if upgrade_check and dialog.confirm("Found new version, do you want to upgrade?", "no"):
        upgrade.upgrade_pull()
        upgrade.upgrade_env()
        upgrade.upgrade_data()
    if not upgrade_check:
        dialog.alert("No upgrade found.")
    exit(0)

def select_list(list_name):
    page_title_list = list()
    page_list = json.loads(file.read_file(list_name))
    i = 1
    if len(page_list) == 0:
        dialog.alert("The page list can not be blank.")
        return [], 0
    for item in page_list:
        page_title_list.append("{}. {}".format(i, item["title"]))
        i += 1
    post_title = dialog.menu("Please select the post to be operated:", page_title_list)
    return page_list, page_title_list.index(post_title)


def get_post_info(title_input="", name_input="", time_input=None):
    title = dialog.prompt("Please enter the title of the article:", title_input).strip()
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return {"title": None, "name": None}
    if name_input == "":
        name_input = get.get_name(title, system_config["Pinyin"])
    name = dialog.prompt("Please enter the slug:", name_input).strip()
    if time_input is not None:
        time_format = "%Y-%m-%d %H:%M:%S"
        time_input_format = time.strftime(time_format, time.localtime(time_input))
        time_input = dialog.prompt("Please enter the time:(Current time zone:{})".format(time.tzname[0]),
                                   time_input_format).strip()
        time.strptime(time_input, time_format)

    return {"title": title, "name": name, "time": time}
