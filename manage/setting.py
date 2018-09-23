#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import time

from common import file
from manage import whiptail

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.title = "SilverBlog settings tool"
system_config = {
    "Project_Name": "",
    "Project_Description": "",
    "Project_URL": "https://",
    "Author_Image": "",
    "Author_Name": "",
    "Author_Introduction": "",
    "Theme": "",
    "API_Password": "",
    "Paging": 10,
    "Time_Format": "%Y-%m-%d",
    "Editor": "nano",
    "i18n": "en-US"
}
if os.path.exists("./config/system.json"):
    system_config = json.loads(file.read_file("./config/system.json"))

def setting_menu():
    while True:
        menu_list = ["Using Setup Wizard", "Using Manual setup",
                     "Theme package manage", "=========================",
                     "Back", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Using Setup Wizard":
            setup_wizard()
        if result == "Using Manual setup":
            manual_setup_list()
        if result == "Theme package manage":
            theme_manage()
        time.sleep(0.5)

def save_config():
    file.write_file("./config/system.json", file.json_format_dump(system_config))

def theme_manage():
    from manage import theme
    dialog.title = "Theme package manager"
    while True:
        menu_list = ["Install the theme", "Use the existing theme", "Upgrade existing theme",
                     "Remove existing theme", "Set insertion point", "=========================", "Back", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        theme_name = ""
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Install the theme":
            install_menu = ["View list", "Enter the theme package name"]
            result = dialog.menu("Please select an action", install_menu)
            if result == "View list":
                org_list = theme.get_orgs_list()
                item_list = list()
                for item in org_list:
                    item_list.append(item["name"])
                theme_name = dialog.menu("Please select the theme you want to install:", item_list)
            if result == "Enter the theme package name":
                theme_name = dialog.prompt("Please enter the theme package name:")
            if len(theme_name) == 0:
                dialog.alert("Theme name cannot be empty")
                continue
            if os.path.exists("./templates/" + theme_name):
                dialog.alert("This theme has been installed.")
                continue
            has_theme = False
            for item in org_list:
                if item["name"].lower() == theme_name.lower():
                    has_theme = True
            if not has_theme:
                dialog.alert("Can not find this theme.")
                continue
            theme.install_theme(theme_name, False)
            if theme_name is not None and dialog.confirm("Do you want to enable this theme now?", "no"):
                system_config["Theme"] = theme_name
                if os.path.exists("./templates/{}/i18n".format(theme_name)):
                    system_config["i18n"] = setting_i18n(theme_name)
                if os.path.exists("./templates/{}/config.json".format(theme_name)):
                    setting_theme_config(theme_name)
            save_config()
        if result == "Use the existing theme":
            theme_name = select_theme()
            system_config["Theme"] = theme_name
            if os.path.exists("./templates/{}/i18n".format(theme_name)):
                system_config["i18n"] = setting_i18n(theme_name)
            if os.path.exists("./templates/{}/config.json".format(theme_name)):
                setting_theme_config(theme_name)
            save_config()
        if result == "Upgrade existing theme":
            theme.upgrade_theme(select_theme())
        if result == "Remove existing theme":
            theme.remove_theme(select_theme())
        if result == "Set insertion point":
            setting_template_insertion()
        time.sleep(0.5)


def manual_setup_list():
    while True:
        menu_list = ["Project name", "Project description", "Access URL", "Remote API password", "Author name",
                     "Author introduction", "Author avatar", "Paging", "Time format", "Editor",
                     "=========================", "Back", "Exit"]
        result = dialog.menu("Please select the item you want to configure", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Project name":
            project_name()
        if result == "Project description":
            project_description()
        if result == "Access URL":
            project_url()
        if result == "Remote API password":
            remote_api_password()
        if result == "Author name":
            author_name()
        if result == "Author introduction":
            author_introduction()
        if result == "Author avatar":
            author_avatar()
        if result == "Paging":
            paging()
        if result == "Time format":
            time_format()
        if result == "Editor":
            editor()
        save_config()
        time.sleep(0.5)


def setting_template_insertion():
    menu_list = ["head", "comment", "foot"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "head":
        os.system("{} ./templates/include/head.html".format(system_config["Editor"]))
    if result == "comment":
        os.system("{} ./templates/include/comment.html".format(system_config["Editor"]))
    if result == "foot":
        os.system("{} ./templates/include/foot.html".format(system_config["Editor"]))


def select_theme():
    from manage import theme
    directories = theme.get_local_theme_list()
    if len(directories) == 0:
        dialog.alert("The Theme list can not be blank.")
        return
    return dialog.menu("Please select the theme to be operated:", directories)
def setting_theme_config(theme_name):
    theme_config = json.loads(file.read_file("./templates/{}/config.json".format(theme_name)))
    for item in theme_config:
        if type(theme_config[item]) == bool:
            status = "no"
            if theme_config[item]:
                status = "yes"
            theme_config[item] = dialog.confirm("Please choose Boolean item [{}]:".format(item), status)
        if type(theme_config[item]) == int:
            theme_config[item] = int(
                dialog.prompt("Please enter Number item [{}]:".format(item), str(theme_config[item])))
        if type(theme_config[item]) == float:
            theme_config[item] = float(
                dialog.prompt("Please enter Number item [{}]:".format(item), str(theme_config[item])))
        if type(theme_config[item]) == str:
            theme_config[item] = str(dialog.prompt("Please enter String item [{}]:".format(item), theme_config[item]))
    file.write_file("./templates/{}/config.json".format(theme_name), file.json_format_dump(theme_config))
    return

def setting_i18n(theme_name):
    dir_list = os.listdir("./templates/{0}/i18n".format(theme_name))
    show_list = list()
    for item in dir_list:
        if item.endswith(".json"):
            show_list.append(item.replace(".json", ""))
    return dialog.menu("Please select the i18n to be operated:", show_list)

def setup_wizard():
    project_name()
    project_description()
    project_url()
    remote_api_password()
    author_name()
    author_introduction()
    author_avatar()
    paging()
    time_format()
    editor()
    save_config()


def project_name():
    item = "Project_Name"
    system_config[item] = dialog.prompt("Please enter the project name:", system_config[item])


def project_description():
    item = "Project_Description"
    system_config[item] = dialog.prompt("Please enter the project description:", system_config[item])


def project_url():
    item = "Project_URL"
    system_config[item] = dialog.prompt("Please enter the access URL:", system_config[item])


def remote_api_password():
    notice = ""
    if system_config["API_Password"] is not "":
        notice = "\n(Leave blank does not change)"
    new_password = dialog.prompt("Please enter the remote api password:" + notice, "",
                                 True)
    if len(new_password) != 0:
        import hashlib
        system_config["API_Password"] = json.dumps(
            {"hash_password": hashlib.md5(new_password.encode('utf-8')).hexdigest()})


def author_name():
    item = "Author_Name"
    system_config[item] = dialog.prompt("Please enter the author name:", system_config[item])


def author_introduction():
    item = "Author_Introduction"
    system_config[item] = dialog.prompt("Please enter the author introduction:", system_config[item])


def author_avatar():
    item = "Author_Image"
    if dialog.confirm("Use Gravatar?", "no"):
        from manage import get
        system_config[item] = get.get_gravatar(system_config["Author_Name"])
    system_config[item] = dialog.prompt("Please enter the author image:", system_config[item])


def paging():
    item = "Paging"
    system_config[item] = int(dialog.prompt("Please enter the paging:", str(system_config[item])))


def time_format():
    item = "Time_Format"
    system_config[item] = dialog.prompt("Please enter the time format:", system_config[item])


def editor():
    item = "Editor"
    editor_name = dialog.prompt("Please enter the editor:", system_config[item])
    result = os.system("which {}".format(editor_name))
    result_code = result >> 8
    if result_code != 0:
        dialog.alert("Warning! This editor may not be installed.")
    system_config[item] = editor_name
