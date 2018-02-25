
import os

import requests

from common import console

def get_orgs_list():
    console.log("info", "Getting the list of theme...")
    try:
        return requests.get("https://api.github.com/orgs/silverblogtheme/repos").json()
    except  requests.exceptions.RequestException:
        console.log("Error", "Get the theme list error.")
        exit(1)

def get_local_theme_list():
    from common import file
    directories = file.list_dirs("./templates")
    if "static" in directories:
        directories.remove("static")
    if "include" in directories:
        directories.remove("include")
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
        return
    r = None
    console.log("info", "Getting the theme installation script...")
    try:
        r = requests.get("https://raw.githubusercontent.com/{}/master/install.sh".format(full_name)).text
    except requests.exceptions.RequestException:
        console.log("Error", "Get the theme installation script error.")
        return
    os.system("cd ./templates \n" + r)
    console.log("Success", "The theme is installed successfully!")
    return name

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
    remote.fetch(repo.active_branch)
    if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD"):
        remote.pull()
        console.log("Success", "The theme is upgrade successfully!")
        return
    console.log("Info", "No upgrade found.")
