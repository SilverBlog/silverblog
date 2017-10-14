import json
import os
import urllib.request

from common import console, file


def get_orgs_list():
    console.log("info", "Getting the list of theme...")
    try:
        return json.loads(
            urllib.request.urlopen("https://api.github.com/orgs/silverblogtheme/repos").read().decode('utf-8'))
    except urllib.error:
        console.log("Error", "Get the topic list error.")
        exit(1)


def get_local_theme_list():
    from common import file
    directories = file.list_dirs("./templates")
    if "static" in directories:
        directories.remove("static")
    return directories
def install_theme(theme_name, orgs_list=None):
    if orgs_list is None:
        orgs_list = get_orgs_list()
    has_theme = False
    full_name = None
    name = None
    for item in orgs_list:
        if item["name"].lower() == theme_name.lower():
            has_theme = True
            full_name = item["full_name"]
            name = item["name"]
    if not has_theme:
        console.log("Error", "Can not find this theme.")
        exit(1)
    r = None
    r_license = None
    console.log("info", "Getting project license...")
    try:
        r_license = urllib.request.urlopen(
            "https://raw.githubusercontent.com/{}/master/LICENSE".format(full_name)).read().decode('utf-8')
    except urllib.error:
        console.log("Error", "Get the project license error.")
        exit(1)
    print("\n{}\n".format(r_license))
    enable_theme = input('I agree to the terms and conditions. [y/N]')
    if enable_theme.lower() == 'yes' or enable_theme.lower() == 'y':
        console.log("info", "Getting the theme installation script...")
        try:
            r = urllib.request.urlopen(
                "https://raw.githubusercontent.com/{}/master/install.sh".format(full_name)).read().decode('utf-8')
        except urllib.error:
            console.log("Error", "Get the theme installation script error.")
            exit(1)
        os.system("cd templates \n" + r)
        enable_theme = input('Do you want to enable this theme now? [y/N]')
        if enable_theme.lower() == 'yes' or enable_theme.lower() == 'y':
            system_info = json.loads(file.read_file("./config/system.json"))
            system_info["Theme"] = name
            file.write_file("./config/system.json",
                            json.dumps(system_info, indent=4, sort_keys=False, ensure_ascii=False))
            console.log("Success", "The theme has been enabled!")
        console.log("Success", "The theme is installed successfully!")


def remove_theme(theme_name):
    import shutil
    shutil.rmtree("./templates/" + theme_name)
    if os.path.exists("./templates/static/" + theme_name):
        shutil.rmtree("./templates/static/" + theme_name)
    console.log("Success", "The theme is uninstalled successfully!")


def upgrade_theme(theme_name):
    import git
    repo = git.Repo("./templates/" + theme_name)
    remote = repo.remote()
    remote.pull()
    console.log("Success", "The theme is upgrade successfully!")
