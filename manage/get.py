import re

import requests

from common import file, console

def get_excerpt(filename):
    content = file.read_file(filename)
    excerpt_output = re.sub('(!\[.*\]\([^)]*\))|(\[.*\]\([^)]*\))|<.+>|\*+|`|#+|-+|>', '', content)
    excerpt = excerpt_output.replace("\n", "")
    if len(excerpt) > 140:
        split_index = 140
        excerpt_output_replace = excerpt_output.replace(".", "。").replace(",", "，")
        newline_index = excerpt_output_replace.find("\n", 140, 240)
        dot_index = excerpt_output_replace.find("。", 140, 240)
        comma_index = excerpt_output_replace.find("，", 140, 240)
        if newline_index != -1:
            split_index = newline_index
        if newline_index == -1 and dot_index != -1:
            split_index = dot_index
        if dot_index == -1 and comma_index != -1:
            split_index = comma_index
        excerpt = excerpt_output[:split_index].replace("\n", "")
    return excerpt

def get_gravatar(author_name):
    r = {"entry": [{"hash": ""}]}
    console.log("info", "Get Gravatar URL...")
    gravatar_hash = ""
    try:
        r = requests.get("https://en.gravatar.com/{0}.json".format(author_name)).json()
        gravatar_hash = r["entry"][0]["hash"]
    except (TypeError, ValueError, requests.exceptions.RequestException):
        console.log("Error", "Get Gravatar URL error,use default avatar.")
    return "https://secure.gravatar.com/avatar/{0}".format(gravatar_hash)

def filter_name(name):
    sub = re.sub('[/:*?<>|\'"\\\]', '', name)
    sub = sub.replace(".", "")
    return sub
