import json
import urllib.error
import urllib.request

from common import console

def get_gavatar(author_name):
    r = {"entry": [{"hash": ""}]}
    console.log("info", "Get Gravatar URL...")
    gravatar_hash = ""
    try:
        r = urllib.request.urlopen(
            "https://en.gravatar.com/{0}.json".format(author_name)).read().decode('utf-8')
        req = json.loads(r)
        gravatar_hash = req["entry"][0]["hash"]
    except (TypeError, ValueError, urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError):
        console.log("Error", "Get Gravatar URL error.")
        exit(1)
    return "https://secure.gravatar.com/avatar/{0}".format(gravatar_hash)
