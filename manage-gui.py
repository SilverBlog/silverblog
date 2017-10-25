#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import time

from common import whiptail, file

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.title = "SilverBlog command line management tool"
def loop():
    menu_list = ["Article manager", "Upgrade", "Theme package manager", "Build static page", "Exit"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "Exit":
        exit(0)
    if result == "Article manager":
        article_manager()
    if result == "Upgrade":
        upgrade()
    if result == "Theme package manager":
        theme_manage()
    if result == "Build static page":
        from manage import build_static_page
        dialog.title = "Build static page"
        build_static_page.publish(dialog.confirm("Push to git?", "no"),
                                  dialog.confirm("Generate a hyperlink with a file extension?", "no"))

def article_manager():
    dialog.title = "Article manager"
    from manage import build_rss, update_post
    menu_list = ["New", "Update", "Edit", "Delete"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "New":
        new_post()
    if result == "Edit":
        edit_post()
    if result == "Delete":
        delete_post()
    if result != "Delete":
        update_post.update()
    build_rss.build_rss()

def upgrade():
    dialog.title = "Upgrade"
    from manage import upgrade
    if upgrade.upgrade_check():
        if dialog.confirm("Find new version, do you want to upgrade?", "no"):
            upgrade.upgrade_pull()
            return
    dialog.alert("No upgrade found")

def edit_post():
    from manage import edit_post
    dialog.title = "Edit post"
    page_list, post_index = select_post()
    config = get_post_info(page_list[post_index]["title"], page_list[post_index]["name"])
    system_info = json.loads(file.read_file("./config/system.json"))
    edit_post.edit(page_list, post_index, config, system_info["Editor"])

def delete_post():
    from manage import delete_post
    page_list, post_index = select_post()
    if dialog.confirm(
            "Are you sure you want to delete this article? (Warning! This operation is irreversible, please be careful!)",
            "no"):
        delete_post.delete(page_list, post_index)

def select_post():
    page_title_list = list()
    page_list = json.loads(file.read_file("./config/page.json"))
    i = 1
    for item in page_list:
        page_title_list.append("{}. {}".format(i, item["title"]))
        i += 1
    post_title = dialog.menu("Please select the post to be operated:", page_title_list)
    return page_list, page_title_list.index(post_title)

def get_post_info(title_input="", name_input=""):
    from manage import new_post
    title = dialog.prompt("Please enter the title of the article:", title_input)
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        return
    if name_input == "":
        name_input = new_post.get_name(title)
    name = dialog.prompt("Please enter the slug:", name_input)
    return {"title": title, "name": name}

def new_post():
    from manage import new_post
    dialog.title = "New post"
    new_post.new_post_init(get_post_info(), dialog.confirm("Is this an independent page?", "no"))

def theme_manage():
    from manage import theme
    dialog.title = "Theme package manager"
    menu_list = ["Install the theme", "Use the existing theme", "Upgrade existing Theme",
                 "Uninstall existing Theme"]
    result = dialog.menu("Please select an action", menu_list)
    theme_name = ""
    orgs_list = None
    if result == "Install the theme":
        install_menu = ["View list", "Enter the theme package name"]
        result = dialog.menu("Please select an action", install_menu)
        if result == "View list":
            orgs_list = theme.get_orgs_list()
            item_list = list()
            for item in orgs_list:
                item_list.append(item["name"])
            theme_name = dialog.menu("Please select the theme you want to install:", orgs_list)
        if result == "Enter the theme package name":
            theme_name = dialog.prompt("Please enter the theme package name:")
        if len(theme_name) != 0:
            theme_name = theme.install_theme(theme_name)
            if dialog.prompt("Do you want to enable this theme now?", "no"):
                theme.set_theme(theme_name)
        return
    directories = theme.get_local_theme_list()
    theme_name = dialog.menu("Please select the theme to be operated:", directories)
    if result == "Use the existing theme":
        theme.set_theme(theme_name)
    if result == "Upgrade existing Theme":
        theme.upgrade_theme(theme_name)
    if result == "Uninstall existing Theme":
        theme.remove_theme(theme_name)

if __name__ == '__main__':
    while True:
        loop()
        time.sleep(0.5)
