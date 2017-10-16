#!/usr/bin/python3
# -*- coding: utf-8 -*-

from common import whiptail
from manage import build_rss, build_static_page, new_post, update_post, theme

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.title = "SilverBlog command line management tool"
menu_list = ["New post", "Update post", "Upgrade", "Theme package manager", "Build static page"]
result = dialog.menu("Please select an action", menu_list)
if result == "New post":
    dialog.title = "New post"
    title = dialog.prompt("Please enter the title of the article:")
    if len(title) == 0:
        dialog.alert("The title can not be blank.")
        exit(1)
    name = dialog.prompt("Please enter the URL (Leave a blank use pinyin):")
    if len(name) == 0:
        name = new_post.get_name(title)
    config = {"title": title, "name": name}
    new_post.new_post_init(config, dialog.confirm("Is this an independent page?", "no"))
    build_rss.build_rss()
    exit(0)
if result == "Upgrade":
    from manage import upgrade

    if upgrade.upgrade_check():
        if dialog.confirm("Find new version, do you want to upgrade?", "no"):
            upgrade.upgrade_pull()
            exit(0)
    dialog.alert("No upgrade found")
    exit(0)
if result == "Update post":
    update_post.update()
    build_rss.build_rss()
    exit(0)
if result == "Theme package manager":
    dialog.title = "Theme package manager"
    menu_list = ["View list", "Enter the theme package name", "Upgrade existing Theme", "Uninstall existing Theme"]
    result = dialog.menu("Please select an action", menu_list)
    theme_name = ""
    orgs_list = None
    if result == "View list":
        orgs_list = theme.get_orgs_list()
        item_list = list()
        for item in orgs_list:
            item_list.append(item["name"])
        theme_name = dialog.menu("Please select the theme you want to install:", item_list)
    if result == "Enter the theme package name":
        theme_name = dialog.prompt("Please enter the theme package name:")
    if len(theme_name) != 0:
        theme.install_theme(theme_name, orgs_list)
        exit(0)
    directories = theme.get_local_theme_list()
    theme_name = dialog.menu("Please select the theme you want to uninstall:", directories)
    if result == "Upgrade existing Theme":
        theme.upgrade_theme(theme_name)
    if result == "Uninstall existing Theme":
        theme.remove_theme(theme_name)
    exit(0)
if result == "Build static page":
    dialog.title = "Build static page"
    build_static_page.publish(dialog.confirm("Push to git?", "no"),
                              dialog.confirm("Generate a hyperlink with a file extension?", "no"))
    exit(0)
