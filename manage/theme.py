import asyncio
import json
import os
import shutil

import requests

from common import console
from common import file


def get_package_list():
    console.log("Info", "Getting the list of theme...")
    try:
        return requests.get("https://api.github.com/orgs/silverblog-theme/repos").json()
    except requests.exceptions.RequestException:
        console.log("Error", "Get the theme list error.")
        exit(1)


def get_local_theme_list():
    directories = file.list_dirs("./templates")
    dir_list = list()
    for item in directories:
        if os.path.exists("./templates/{}/.git".format(item)):
            dir_list.append(item)
    return dir_list


def get_package_info(package_url):
    try:
        return requests.get(package_url).text
    except requests.exceptions.RequestException:
        return None


def install_theme(theme_name, custom):
    import git
    if not os.path.exists("./templates/static"):
        os.mkdir("./templates/static")
    repo_dir = "./templates/{}".format(theme_name)
    if os.path.exists(repo_dir):
        console.log("Error", "This theme has been installed.")
        exit(1)
    console.log("Info", "Get the theme repository...")
    git_repo = "https://github.com/silverblog-theme/{}.git".format(theme_name)
    if custom:
        git_repo = theme_name
    try:
        git.Repo.clone_from(url=git_repo, to_path=repo_dir, depth=1)
    except git.exc.GitCommandError:
        console.log("Error", "Unable to clone theme repository.")
        exit(1)
    if os.path.exists("{}/package-metadata.json".format(repo_dir)):
        config_example_file = "{}/config.example.json".format(repo_dir)
        static_symlink = "./templates/static/{}".format(theme_name)

        if not os.path.exists(static_symlink):
            os.symlink("{}/templates/{}/static".format(os.getcwd(), theme_name), static_symlink)

        if os.path.exists(config_example_file):
            shutil.copyfile(config_example_file, "{}/config.json".format(repo_dir))

        download_static_file(theme_name)
    if not os.path.exists("{}/package-metadata.json".format(repo_dir)) and os.path.exists("{}/install.sh".format(repo_dir)):
        result_code = os.system("cd templates && bash {}/install.sh".format(theme_name))
        if (result_code >> 8) != 0:
            console.log("Error", "An error occurred while executing the install script.")
            exit(1)
    console.log("Success", "The theme is install successfully!")


def remove_theme(theme_name):
    static_symlink = "./templates/static/{}".format(theme_name)
    if os.path.exists(static_symlink):
        os.remove(static_symlink)

    shutil.rmtree("./templates/" + theme_name)
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
            if os.path.exists("./templates/{}/package-metadata.json".format(theme_name)):
                download_static_file(theme_name)
            console.log("Success", "The theme is upgrade successfully!")
            return
    console.log("Info", "No upgrade found.")


def download_static_file(theme_name):
    if not os.path.exists("./templates/{}/package-metadata.json".format(theme_name)):
        return
    download_list_file = "./templates/{}/package-metadata.json".format(theme_name)
    download_file_location = "./templates/{}/static/library".format(theme_name)
    if os.path.exists(download_file_location):
        shutil.rmtree(download_file_location)
    os.mkdir(download_file_location)
    package_info = json.loads(file.read_file(download_list_file))

    download_list = list()
    if "download" in package_info:
        download_list = package_info["download"]

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


def get_readme(theme_name):
    console.log("Info", "Getting the readme of theme...")
    try:
        r = requests.get("https://raw.githubusercontent.com/silverblog-theme/{}/master/README.md".format(theme_name))
        return r.text
    except requests.exceptions.RequestException:
        console.log("Error", "Get the readme error.")
        exit(1)