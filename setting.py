#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from common import whiptail

dialog = whiptail.Whiptail()
dialog.title = "SilverBlog settings management tool"
system_config = {
    "Project_Name": "",
    "Project_Description": "",
    "Project_URL": "",
    "Author_Image": "",
    "Author_Name": "",
    "Author_Introduction": "",
    "Theme": "",
    "API_Password": "",
    "Paging": 10,
    "Time_Format": "%Y-%m-%d",
    "Rss_Full_Content": True,
    "Editor": "vim"
}
if os.path.exists("./config/system.json"):

def loop():
    menu_list = ["Use the Setup Wizard", "Set up basic information", "Set up author information", "Other settings",
                 "Exit"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "Use the Setup Wizard":
        setup_wizard()
        return
    if result == "Set up basic information":
        project_info()
        return
    if result == "Set up author information":
        author_info()
        return
    if result == "Other settings":
        outher_info()
        return
    if result == "Exit":
        exit(0)

def setup_wizard():
    project_info()
    author_info()
    if system_config["Theme"] == "":
        from manage import theme
        local_theme_list = theme.get_local_theme_list()
        if len(local_theme_list) != 0:
            system_config["Theme"] = dialog.menu("Please select the theme to be operated:", local_theme_list)
            return
        orgs_list = theme.get_orgs_list()
        item_list = list()
        for item in orgs_list:
            item_list.append(item["name"])
        theme_name = dialog.menu("Please select the theme you want to install:", item_list)
        system_config["Theme"] = theme.install_theme(theme_name, orgs_list)

def show_prompt(items):
    for item in items:
        system_config[item["name"]] = dialog.prompt("Please enter the {}:".format(item["info"]),
                                                    system_config[item["name"]])

def project_info():
    items = [{"name": "Project_Name", "info": "blog name"}, {"name": "Project_Description", "info": "blog description"},
             {"name": "Project_URL", "info": "blog access URL"}]
    show_prompt(items)
    system_config["API_Password"] = dialog.prompt("Please enter the remote management tool password:",
                                                  system_config["API_Password"], True)

def author_info():
    items = [{"name": "Author_Name", "info": "author name"},
             {"name": "Author_Introduction", "info": "author introduction"}]
    show_prompt(items)
    if dialog.confirm("Use Gavatar?", "no"):
        from manage import get_gavatar
        system_config["Author_Image"] = get_gavatar.get_gavatar(system_config["Author_Name"])
        return
    system_config["Author_Image"] = dialog.prompt("Please enter the author image:", system_config["Author_Image"])
def outher_info():
    items = [{"name": "Paging", "info": "paging"}, {"name": "Time_Format", "info": "time format"},
             {"name": "Editor", "info": "editor"}]
    show_prompt(items)
    system_config["Rss_Full_Content"] = dialog.confirm("Output full text Rss?", "yes")

while True:
    loop_ui()
    time.sleep(0.5)
