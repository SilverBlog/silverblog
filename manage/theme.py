import os

import requests

from common import console


def get_orgs_list():
    console.log("Info", "Getting the list of theme...")
    try:
        return requests.get("https://api.github.com/orgs/silverblog-theme/repos").json()
    except  requests.exceptions.RequestException:
        console.log("Error", "Get the theme list error.")
        exit(1)

def get_local_theme_list():
    from common import file
    directories = file.list_dirs("./templates")
    dir_list = list()
    for item in directories:
        if os.path.exists("./templates/{}/.git".format(item)):
            dir_list.append(item)
    return dir_list


def install_theme(name, custom):
    if not os.path.exists("./templates/static"):
        os.mkdir("./templates/static")
    if os.geteuid() == 0:
        running_in_root = input('Running this script as root can damage your system. Continue to execute? [y/N]')
        if running_in_root.lower() != 'y':
            exit(0)
    console.log("Info", "Getting the theme installation script...")
    install_script_url = "https://raw.githubusercontent.com/silverblog-theme/{}/master/install.sh".format(name)
    if custom:
        install_script_url = name
    try:
        r = requests.get(install_script_url).text
    except requests.exceptions.RequestException:
        console.log("Error", "Get the theme installation script error.")
        exit(1)
    result_code = os.system("cd ./templates \n" + r)
    if (result_code >> 8) != 0:
        console.log("Error", "An error occurred while executing the install script.")
        exit(1)
    console.log("Success", "The theme is install successfully!")

def remove_theme(theme_name):
    import shutil
    shutil.rmtree("./templates/" + theme_name)
    if os.path.exists("./templates/static/" + theme_name):
        shutil.rmtree("./templates/static/" + theme_name)
    console.log("Success", "The theme is removed successfully!")

def upgrade_theme(theme_name):
    console.log("Info", "Updating theme, please wait...")
    import git
    repo = git.Repo("./templates/" + theme_name)
    remote = repo.remote()
    remote.fetch(repo.active_branch)
    if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD"):
        remote.pull()
        console.log("Success", "The theme is upgrade successfully!")
        return
    console.log("Info", "No upgrade found.")
