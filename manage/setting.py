#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import time

from common import file
from manage import whiptail

dialog = whiptail.Whiptail()
dialog.height = 15
dialog.backtitle = "SilverBlog management tool"
system_config = {
    "Project_Name": "",
    "Project_Description": "",
    "Project_URL": "https://",
    "Author_Image": "",
    "Author_Name": "",
    "Author_Introduction": "",
    "Theme": "",
    "Paging": 10,
    "Time_Format": "%Y-%m-%d",
    "Editor": "nano",
    "i18n": "en-US",
    "Pinyin": False,
    "Use_CDN": False,
    "Lazyload": False
}
if os.path.exists("./config/system.json"):
    system_config = json.loads(file.read_file("./config/system.json"))


def setting_menu(main_run=False):
    while True:
        dialog.title = "Setting"
        menu_list = ["Using Setup Wizard", "Using Manual setup",
                     "Theme package manage", "Create a backup", "=" * 25,
                     ]
        if not main_run:
            menu_list.append("Back")
        menu_list.append("Exit")

        result = dialog.menu("Please select an action", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Create a backup":
            from manage import backup
            backup.backup()
            dialog.alert("The backup is complete.")
        if result == "Using Setup Wizard":
            setup_wizard()
        if result == "Using Manual setup":
            manual_setup_list()
        if result == "Theme package manage":
            theme_manage()

def save_config():
    file.write_file("./config/system.json", file.json_format_dump(system_config))

def theme_manage():
    from manage import theme
    dialog.title = "Theme package manager"
    while True:
        menu_list = ["Install the theme", "Use the existing theme", "Upgrade existing theme",
                     "Remove existing theme", "Set insertion point", "=" * 25, "Back", "Exit"]
        result = dialog.menu("Please select an action", menu_list)
        theme_name = ""
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Install the theme":
            install_menu = ["View list", "Enter the theme package name"]
            result = dialog.menu("Please select an action", install_menu)
            org_list = theme.get_orgs_list()
            if result == "View list":
                item_list = list()
                for item in org_list:
                    item_list.append(item["name"])
                theme_name = dialog.menu("Please select the theme you want to install:", item_list)
            if result == "Enter the theme package name":
                theme_name = dialog.prompt("Please enter the theme package name:")
            if len(theme_name) == 0:
                dialog.alert("Theme name cannot be empty")
                continue
            has_theme = False
            for item in org_list:
                if item["name"].lower() == theme_name.lower():
                    has_theme = True
            if not has_theme:
                dialog.alert("Can not find this theme.")
                continue
            readme = theme.get_readme(theme_name)
            if readme is not None:
                dialog.alert_muilt_line(readme)
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
            theme.download_static_file(theme_name)
            save_config()
        if result == "Upgrade existing theme":
            theme.upgrade_theme(select_theme())
        if result == "Remove existing theme":
            theme_name = select_theme()
            if theme_name is None:
                continue
            if system_config["Theme"] == theme_name:
                dialog.alert("This theme is in use and cannot be removed.")
                continue
            theme.remove_theme(theme_name)
        if result == "Set insertion point":
            setting_template_insertion()
        time.sleep(0.5)


def manual_setup_list():
    while True:
        dialog.title = "Manual setup"
        menu_list = ["Project name", "Project description", "Access URL", "Remote API password", "Author name",
                     "Author introduction", "Author avatar", "Paging", "Time format", "Editor", "Use CDN","Image lazyload"
                     "Automatically convert Chinese characters to pinyin",
                     "=" * 50, "Back", "Exit"]
        result = dialog.menu("Please select the item you want to configure", menu_list)
        if result == "Exit":
            exit(0)
        if result == "Back":
            break
        if result == "Project name":
            set_string("Project_Name", "Please enter the project name:")
        if result == "Project description":
            set_string("Project_Description", "Please enter the project description:")
        if result == "Access URL":
            set_string("Project_URL", "Please enter the access URL:")
        if result == "Remote API password":
            remote_api_password()
        if result == "Author name":
            set_string("Author_Name", "Please enter the author name:")
        if result == "Author introduction":
            set_string("Author_Introduction", "Please enter the author introduction:")
        if result == "Author avatar":
            author_avatar()
        if result == "Paging":
            set_int("Paging", "Please enter the paging:")
        if result == "Time format":
            set_string("Time_Format", "Please enter the time format:")
        if result == "Editor":
            editor()
        if result == "Use CDN":
            set_bool("Use_CDN", "Use CDN?")
        if result == "Lazyload":
            set_bool("Image lazyload", "Use image lazyload?")
        if result == "Automatically convert Chinese characters to pinyin":
            set_bool("Pinyin", "Use automatic conversion of Chinese characters to Pinyin?")
        save_config()
        time.sleep(0.5)


def setting_template_insertion():
    menu_list = ["head", "comment", "footer", "Page foot"]
    result = dialog.menu("Please select an action", menu_list)
    if result == "head":
        os.system("{} ./templates/include/head.html".format(system_config["Editor"]))
    if result == "comment":
        os.system("{} ./templates/include/comment_box.html".format(system_config["Editor"]))
    if result == "footer":
        os.system("{} ./templates/include/footer.html".format(system_config["Editor"]))
    if result == "Page foot":
        os.system("{} ./templates/include/foot.html".format(system_config["Editor"]))


def select_theme():
    from manage import theme
    directories = theme.get_local_theme_list()
    if len(directories) == 0:
        dialog.alert("The Theme list can not be blank.")
        return None
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
    set_string("Project_Name", "Please enter the project name:")
    set_string("Project_Description", "Please enter the project description:")
    set_string("Project_URL", "Please enter the access URL:")
    remote_api_password()
    set_string("Author_Name", "Please enter the author name:")
    set_string("Author_Introduction", "Please enter the author introduction:")
    author_avatar()
    set_int("Paging", "Please enter the paging:")
    set_string("Time_Format", "Please enter the time format:")
    editor()
    set_bool("Use_CDN", "Use CDN?")
    set_bool("Lazyload", "Use image lazyload?")
    set_bool("Pinyin", "Use automatic conversion of Chinese characters to Pinyin?")
    save_config()


def set_string(item, message):
    system_config[item] = dialog.prompt(message, system_config[item])


def set_int(item, message):
    system_config[item] = int(dialog.prompt(message, str(system_config[item])))


def set_bool(item, message):
    status = "no"
    if system_config[item]:
        status = "yes"
    system_config[item] = dialog.confirm(message, status)



def remote_api_password():
    notice = ""
    if os.path.exists("./config/control.json"):
        notice = "\n(Leave blank does not change)"
    while True:
        new_password = dialog.prompt("Please enter the remote api password:" + notice, "", True)
        if notice != "" and len(new_password) == 0:
            break
        if len(new_password) >= 8:
            break
        dialog.alert("The new password is too weak. Please retry with a stronger combination.")
    if len(new_password) != 0:
        import hashlib
        import hmac
        md5_new_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        sha256_new_password = hmac.new(str("SiLvErBlOg").encode('utf-8'), str(md5_new_password).encode('utf-8'),
                                       hashlib.sha256).hexdigest()
        file.write_file("./config/control.json", json.dumps({"password": sha256_new_password}))



def author_avatar():
    item = "Author_Image"
    if dialog.confirm("Use Gravatar?", "no"):
        from manage import get
        system_config[item] = get.get_gravatar(system_config["Author_Name"])
    system_config[item] = dialog.prompt("Please enter the author image:", system_config[item])

def editor():
    item = "Editor"
    editor_name = dialog.prompt("Please enter the editor:", system_config[item])
    result = os.system("which {}".format(editor_name))
    result_code = result >> 8
    if result_code != 0:
        dialog.alert("Warning! This editor may not be installed.")
    system_config[item] = editor_name
