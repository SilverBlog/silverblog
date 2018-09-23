#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import time

from common import file, console
from manage import whiptail, upgrade, get

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.title = "SilverBlog management tool"
def use_whiptail_mode():
    dialog.title = "SilverBlog management tool"
    menu_list = ["Article manager", "Menu manager", "Build static page", "Setting", "=========================", "Exit"]
    upgrade_text = None
    if os.path.exists("./.git"):
        upgrade_text = "Upgrade"
        upgrade_check = False
        last_fetch_time = 0
        if os.path.exists("./upgrade/last_fetch_time.json"):
            last_fetch_time = json.loads(file.read_file("./upgrade/last_fetch_time.json"))["last_fetch_time"]
        if upgrade.upgrade_check(False):
            upgrade_text = "⚠ Upgrade"
            upgrade_check = True
        if (time.time() - last_fetch_time) > 259200 and not upgrade_check:
            console.log("info", "Checking for updates...")
            file.write_file("./upgrade/last_fetch_time.json", json.dumps({"last_fetch_time": time.time()}))
            if upgrade.upgrade_check():
                upgrade_text = "⚠ Upgrade"
        menu_list = ["Article manager", "Menu manager", "Build static page", upgrade_text, "Setting",
                     "=========================", "Exit"]
    while True:
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Article manager":
            article_manager()
        if result == "Menu manager":
            menu_manager()
        if upgrade_text is not None:
            if result == upgrade_text:
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
    dialog.title = "Article manager"
    while True:
        from manage import build_rss, post_manage
        menu_list = ["New", "Update", "Edit", "Delete", "=========================", "Back", "Exit"]
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
                config = get_post_info(page_list[post_index]["title"], page_list[post_index]["name"])
                system_info = json.loads(file.read_file("./config/system.json"))
                post_manage.edit_post(page_list, post_index, config, system_info["Editor"])
            post_manage.update_post()
        if result == "Delete":
            page_list, post_index = select_list("./config/page.json")
            if page_list and dialog.confirm(
                    "Are you sure you want to delete this article? (Warning! This operation is irreversible, please be careful!)",
                    "no"):
                post_manage.delete_post(page_list, post_index)
        if result == "Update":
            post_manage.update_post()
        build_rss.build_rss()
        time.sleep(0.5)

def menu_manager():
    dialog.title = "Menu manager"
    menu_list = ["New", "Edit", "Delete", "=========================", "Back", "Exit"]
    result = dialog.menu("Please select an action", menu_list)
    while True:
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        from manage import menu_manage
        if result == "New":
            menu_info = get_menu_info()
            if menu_info["title"] is not None:
                menu_manage.add_menu(menu_info)
        if result == "Edit":
            menu_list, menu_index = select_list("./config/menu.json")
            if menu_list:
                menu_item = menu_list[menu_index]
                if "name" in menu_item:
                    address = menu_item["name"]
                    independent = True
                if "absolute" in menu_item:
                    address = menu_item["absolute"]
                    independent = False
                menu_info = get_menu_info(menu_item["title"], address, independent)
                menu_manage.edit_menu(menu_list, menu_index, menu_info)
        if result == "Delete":
            menu_list, select_index = select_list("./config/menu.json")
            if menu_list and dialog.confirm(
                    "Are you sure you want to delete this item? (Warning! This operation is irreversible, please be careful!)",
                    "no"):
                menu_manage.delete_menu(menu_list, select_index)
        time.sleep(0.5)


def get_menu_info(title_input="", name_input="", independent=False):
    title = dialog.prompt("Please enter the title of the menu:", title_input).strip()
    is_independent = "no"
    if independent:
        is_independent = "yes"
    type = dialog.confirm("Is this an independent page?", is_independent)
    name = None
    if type and dialog.confirm("Does this article exist in the list of articles?", "no"):
        page_list, page_index = select_list("./config/page.json")
        name = page_list[page_index]["name"]
    if name is None:
        if not type and name_input == "":
            name_input = "https://"
        name = dialog.prompt("Please enter the address:", name_input).strip()
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return {"title": None, "name": None, "type": False}
    if len(name) == 0:
        dialog.alert("The name can not be blank.")
        return {"title": None, "name": None, "type": False}
    return {"title": title, "name": name, "type": type}

def upgrade_system():
    from manage import upgrade
    dialog.title = "Upgrade"
    if upgrade.upgrade_check() and dialog.confirm("Find new version, do you want to upgrade?", "no"):
        upgrade.upgrade_pull()
        return
    dialog.alert("No upgrade found.")


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


def get_post_info(title_input="", name_input=""):
    title = dialog.prompt("Please enter the title of the article:", title_input).strip()
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return {"title": None, "name": None}
    if name_input == "":
        name_input = get.get_name(title)
    name = dialog.prompt("Please enter the slug:", name_input).strip()
    return {"title": title, "name": name}

def use_text_mode(args):
    if args.command == "qrcode":
        system_config = json.loads(file.read_file("./config/system.json"))
        from common import install_module
        install_module.install_and_import("qrcode_terminal")
        import qrcode_terminal
        if len(system_config["API_Password"]) == 0 or len(system_config["Project_URL"]) == 0:
            console.log("Error", "Check the API_Password and Project_URL configuration items")
            exit(1)
        try:
            password_md5 = json.loads(system_config["API_Password"])["hash_password"]
        except (ValueError, KeyError, TypeError):
            exit(1)
        console.log("Info", "Please use the client to scan the following QR Code")
        config_json = json.dumps({"url": system_config["Project_URL"], "password": password_md5})
        qrcode_terminal.draw(config_json)
        exit(0)
    if args.command == "upgrade":
        from manage import upgrade
        if upgrade.upgrade_check():
            if not args.yes:
                start_to_pull = input('Find new version, do you want to upgrade? [y/N]')
            if start_to_pull.lower() == 'yes' or start_to_pull.lower() == 'y' or args.yes:
                upgrade.upgrade_pull()
                exit(0)
        console.log("info", "No upgrade found")
        exit(0)
    if args.command == "build-page":
        from manage import build_static_page
        build_static_page.publish()
        exit(0)
    from manage import build_rss, post_manage
    if args.command == "new":
        config = None
        if args.config is not None:
            config = json.loads(file.read_file(args.config))
        if config is None:
            print("Please enter the title of the article:")
            title = input().strip()
            if len(title) == 0:
                console.log("Error", "The title can not be blank.")
                exit(1)
            name = get.get_name(title)
            print("Please enter the slug [{}]:".format(name))
            name2 = input().strip()
            if len(name2) != 0:
                name = get.filter_name(name2)
            if os.path.exists("./document/{}.md".format(name)):
                console.log("Error", "File [./document/{}.md] already exists".format(name))
                exit(1)
        if len(name) != 0 and len(title) != 0:
            config = {"title": title, "name": name}
            post_manage.new_post(config, args.independent)
            build_rss.build_rss()
        exit(0)
    if args.command == "update":
        if post_manage.update_post():
            build_rss.build_rss()
        exit(0)