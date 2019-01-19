import asyncio
import json
import os
import shutil

import requests

from common import console
from common import file


def get_orgs_list():
    console.log("Info", "Getting the list of theme...")
    try:
        return requests.get("https://api.github.com/orgs/silverblogtheme/repos").json()
    except  requests.exceptions.RequestException:
        console.log("Error", "Get the theme list error.")
        exit(1)

def get_local_theme_list():
    directories = file.list_dirs("./templates")
    dir_list = list()
    for item in directories:
        if os.path.exists("./templates/{}/.git".format(item)):
            dir_list.append(item)
    return dir_list


def get_readme(name):
    readme_url = "https://raw.githubusercontent.com/silverblogtheme/{}/master/README.md".format(name)
    try:
        return requests.get(readme_url).text
    except requests.exceptions.RequestException:
        return None

def install_theme(name, custom):
    if not os.path.exists("./templates/static"):
        os.mkdir("./templates/static")
    if os.geteuid() == 0:
        running_in_root = console.log("Error",
                                      'Running this script as root can damage your system.Please do not do this.')
        exit(1)
    if os.path.exists("./templates/" + name):
        console.log("Error", "This theme has been installed.")
        exit(1)
    console.log("Info", "Getting the theme installation script...")
    install_script_url = "https://raw.githubusercontent.com/silverblogtheme/{}/master/install.sh".format(name)
    if custom:
        install_script_url = name
    try:
        r = requests.get(install_script_url)
        r.raise_for_status()
        result_script = r.text
    except requests.exceptions.HTTPError as err:
        console.log("Error", err)
        exit(1)
    except requests.exceptions.RequestException:
        console.log("Error", "Get the theme installation script error.")
        exit(1)
    result_code = os.system("cd ./templates \n" + result_script)
    if (result_code >> 8) != 0:
        console.log("Error", "An error occurred while executing the install script.")
        exit(1)
    download_static_file(name)
    console.log("Success", "The theme is install successfully!")

def remove_theme(theme_name):
    shutil.rmtree("./templates/" + theme_name)
    if os.path.exists("./templates/static/" + theme_name):
        shutil.rmtree("./templates/static/" + theme_name)
    console.log("Success", "The theme is removed successfully!")

def upgrade_theme(theme_name):
    import git
    if os.system('cd ./templates/{} && git rev-parse 2> /dev/null > /dev/null'.format(theme_name)) == 0:
        repo = git.Repo("./templates/" + theme_name)
        remote = repo.remote()
        remote.fetch(repo.active_branch)
        if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD"):
            console.log("Info", "Updating theme, please wait...")
            remote.pull()
            download_static_file(theme_name)
            console.log("Success", "The theme is upgrade successfully!")
            return
    console.log("Info", "No upgrade found.")


def download_static_file(theme_name):
    download_list_file = "./templates/{}/cdn/download.json".format(theme_name)
    download_file_location = "./templates/{}/static/library".format(theme_name)
    if not os.path.exists(download_list_file):
        return
    if os.path.exists(download_file_location):
        shutil.rmtree(download_file_location)
    os.mkdir(download_file_location)
    download_list = json.loads(file.read_file(download_list_file))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [download_file(item, download_file_location) for item in download_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


@asyncio.coroutine
def get_file(url):
    console.log("info", "Downloading file:" + url)
    return requests.get(url)


@asyncio.coroutine
def download_file(item, location):
    result = yield from get_file(item["url"])
    write_path = location
    if "path" in item and item["path"] != "":
        write_path = "{}/{}".format(location, item["path"])
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    yield from file.async_write_binary_file("{}/{}".format(write_path, item["filename"]), result.content)
