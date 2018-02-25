import requests

from common import console

def get_gavatar(author_name):
    r = {"entry": [{"hash": ""}]}
    console.log("info", "Get Gravatar URL...")
    gravatar_hash = ""
    try:
        r = requests.get("https://en.gravatar.com/{0}.json".format(author_name)).json()
        gravatar_hash = r["entry"][0]["hash"]
    except (TypeError, ValueError, requests.exceptions.RequestExceptiona):
        console.log("Error", "Get Gravatar URL error.")
    return "https://secure.gravatar.com/avatar/{0}".format(gravatar_hash)
