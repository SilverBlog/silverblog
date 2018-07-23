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
    while True:
        upgrade_text = "Upgrade"
        upgrade_check = False
        last_fetch_time = 0
        if os.path.exists("./upgrade/last_fetch_time.json"):
            last_fetch_time = json.loads(file.read_file("./upgrade/last_fetch_time.json"))["last_fetch_time"]
        if upgrade.upgrade_check(False):
            upgrade_text = "⚠ Upgrade"
            upgrade_check = True
        if (time.time() - last_fetch_time) > 259200 and not upgrade_check:
            file.write_file("./upgrade/last_fetch_time.json", json.dumps({"last_fetch_time": time.time()}))
            if upgrade.upgrade_check():
                upgrade_text = "⚠ Upgrade"

        menu_list = ["Article manager", "Menu manager", "Build static page", upgrade_text, "Setting", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Article manager":
            article_manager()
        if result == "Menu manager":
            menu_manager()
        if result == upgrade_text:
            upgrade_system()
        if result == "Build static page":
            from manage import build_static_page
            dialog.title = "Build static page"
            build_static_page.publish()
        if result == "Setting":
            from manage import setting
            setting.setting_menu()
        time.sleep(0.5)

def article_manager():
    dialog.title = "Article manager"
    from manage import build_rss, update_post
    menu_list = ["New", "Update", "Edit", "Delete"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "New":
        from manage import new_post
        dialog.title = "New post"
        post_info = get_post_info()
        if post_info["name"] is not None:
            new_post.new_post_init(post_info, dialog.confirm("Is this an independent page?", "no"))
    if result == "Edit":
        from manage import edit_post
        dialog.title = "Edit post"
        page_list, post_index = select_list("./config/page.json")
        if not page_list:
            return
        config = get_post_info(page_list[post_index]["title"], page_list[post_index]["name"])
        system_info = json.loads(file.read_file("./config/system.json"))
        edit_post.edit(page_list, post_index, config, system_info["Editor"])
        if not update_post.update():
            return
    if result == "Delete":
        from manage import delete_post
        page_list, post_index = select_list("./config/page.json")
        if page_list and dialog.confirm(
                "Are you sure you want to delete this article? (Warning! This operation is irreversible, please be careful!)",
                "no"):
            delete_post.delete(page_list, post_index)
    if result == "Update":
        if not update_post.update():
            return
    build_rss.build_rss()


def menu_manager():
    dialog.title = "Menu manager"
    menu_list = ["New", "Edit", "Delete"]
    result = dialog.menu("Please select an action", menu_list)
    from manage import menu_manage
    if result == "New":
        menu_info = get_menu_info()
        if menu_info["title"] is not None:
            menu_manage.add_menu(menu_info)
        return
    if result == "Edit":
        menu_list, menu_index = select_list("./config/menu.json")
        if not menu_list:
            return
        menu_item = menu_list[menu_index]
        if "name" in menu_item:
            address = menu_item["name"]
            independent = True
        if "absolute" in menu_item:
            address = menu_item["absolute"]
            independent = False
        menu_info = get_menu_info(menu_item["title"], address, independent)
        menu_manage.edit_menu(menu_list, menu_index, menu_info)
        return
    if result == "Delete":
        menu_list, select_index = select_list("./config/menu.json")
        if menu_list and dialog.confirm(
                "Are you sure you want to delete this item? (Warning! This operation is irreversible, please be careful!)",
                "no"):
            menu_manage.delete_menu(menu_list, select_index)
        return


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
        try:
            import qrcode_terminal
        except ImportError:
            console.log("Error", "Please install the qrcode-terminal package to support this feature")
            install_dependency = input('Do you want to install qrcode-terminal now? [y/N]')
            if install_dependency.lower() == 'yes' or install_dependency.lower() == 'y':
                import os
                os.system("python3 -m pip install qrcode-terminal")
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
    from manage import build_rss
    if args.command == "new":
        from manage import new_post
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
        if len(name) != 0 and len(title) != 0:
            config = {"title": title, "name": name}
            new_post.new_post_init(config, args.independent)
            build_rss.build_rss()
        exit(0)
    if args.command == "update":
        from manage import update_post
        if update_post.update():
            build_rss.build_rss()
        exit(0)