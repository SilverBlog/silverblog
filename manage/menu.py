#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import time

from common import file, console
from manage import whiptail

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.title = "SilverBlog management tool"
def use_whiptail_mode():
    dialog.title = "SilverBlog management tool"
    while True:
        upgrade_text = "Upgrade"
        last_fetch_time = 0
        if os.path.exists("./upgrade/last_fetch_time.json"):
            last_fetch_time = json.loads(file.read_file("./upgrade/last_fetch_time.json"))["last_fetch_time"]
        if (time.time() - last_fetch_time) > 604800:
            from manage import upgrade
            file.write_file("./upgrade/last_fetch_time.json", json.dumps({"last_fetch_time": time.time()}))
            if upgrade.upgrade_check():
                upgrade_text = "⚠ Upgrade"

        menu_list = ["Article manager", "Build static page", upgrade_text, "Setting", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Article manager":
            article_manager()
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
        new_post()
    if result == "Edit":
        edit_post()
        if not update_post.update():
            return
    if result == "Delete":
        delete_post()
    if result == "Update":
        if not update_post.update():
            return
    build_rss.build_rss()


def upgrade_system():
    from manage import upgrade
    dialog.title = "Upgrade"
    if upgrade.upgrade_check() and dialog.confirm("Find new version, do you want to upgrade?", "no"):
        upgrade.upgrade_pull()
        return
    dialog.alert("No upgrade found.")

def edit_post():
    from manage import edit_post
    dialog.title = "Edit post"
    page_list, post_index = select_post()
    if not page_list:
        return
    config = get_post_info(page_list[post_index]["title"], page_list[post_index]["name"])
    system_info = json.loads(file.read_file("./config/system.json"))
    edit_post.edit(page_list, post_index, config, system_info["Editor"])

def delete_post():
    from manage import delete_post
    page_list, post_index = select_post()
    if page_list and dialog.confirm(
            "Are you sure you want to delete this article? (Warning! This operation is irreversible, please be careful!)",
            "no"):
        delete_post.delete(page_list, post_index)

def select_post():
    page_title_list = list()
    page_list = json.loads(file.read_file("./config/page.json"))
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
    title = dialog.prompt("Please enter the title of the article:", title_input)
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return
    if name_input == "":
        from manage import get
        name_input = get.get_name(title)
    name = dialog.prompt("Please enter the slug:", name_input)
    return {"title": title, "name": name}

def new_post():
    from manage import new_post
    dialog.title = "New post"
    new_post.new_post_init(get_post_info(), dialog.confirm("Is this an independent page?", "no"))

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
            start_to_pull = input('Find new version, do you want to upgrade? [y/N]')
            if start_to_pull.lower() == 'yes' or start_to_pull.lower() == 'y':
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
            title = input()
            if len(title) != 0:
                name = get.get_name(title)
            print("Please enter the slug [{}]:".format(name))
            name2 = input()
            if len(name2) != 0:
                name = name2
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