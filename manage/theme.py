import urllib.request

from common import console


def get_theme_list():
    console.log("info", "Get Theme List")
    r = "[]"
    try:
        r = urllib.request.urlopen("https://api.github.com/orgs/silverblogtheme/repos").read().decode('utf-8')
    except urllib2.HTTPError:
        console.log("Error", "Get Theme List error")
        exit(1)
    req = json.loads(r)
    for item in req:
        print("Name:{0} Description:{1} Star{2}".format(item["name"], item["description"], item["stargazers_count"]))
