import json
import os
import urllib.request

from common import console, file


def get_orgs_list():
    console.log("info", "Getting the list of theme...")
    r = "[]"
    try:
        r = urllib.request.urlopen("https://api.github.com/orgs/silverblogtheme/repos").read().decode('utf-8')
    except urllib2.HTTPError:
        console.log("Error", "Get the topic list error.")
        exit(1)
    return json.loads(r)

def get_theme_list():
    req = get_orgs_list()
    for item in req:
        print("-" * 100)
        print(
            " Name:{0}\n Description:{1}\n Star:{2}".format(item["name"], item["description"],
                                                            item["stargazers_count"]))
        print("-" * 100)


def install_theme(theme_name):
    req = get_orgs_list()
    has_theme = False
    full_name = None
    name = None
    for item in req:
        if item["name"].lower() == theme_name.lower():
            has_theme = True
            full_name = item["full_name"]
            name = item["name"]
    if not has_theme:
        console.log("Error", "Can not find this theme.")
        return
    r = ""
    console.log("info", "Getting the theme installation script...")
    try:
        r = urllib.request.urlopen(
            "https://raw.githubusercontent.com/{}/master/install.sh".format(full_name)).read().decode('utf-8')
    except urllib2.HTTPError:
        console.log("Error", "Get the theme installation script error.")
        exit(1)
    os.system("cd templates \n" + r)
    enable_theme = input('Do you want to enable this theme now? [y/N]')
    if enable_theme.lower() == 'yes' or enable_theme.lower() == 'y':
        system_info = json.loads(file.read_file("./config/system.json"))
        system_info["Theme"] = name
        file.write_file("./config/system.json", json.dumps(system_info))
        console.log("Success", "The theme has been enabled!")
    console.log("Success", "The theme is installed successfully!")

