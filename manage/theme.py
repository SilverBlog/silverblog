import json
import os
import urllib.request

from common import console


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
        print(
            "------------------------------\n Name:{0}\n Description:{1}\n Star:{2}\n------------------------------\n".format(
                item["name"],
                item["description"],
                item[
                                                                                                   "stargazers_count"]))


def install_theme(theme_name):
    req = get_orgs_list()
    has_theme = False
    full_name = None
    for item in req:
        if item["name"] == theme_name:
            has_theme = True
            full_name = item["full_name"]
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
    console.log("Success", "The theme is installed successfully!")
