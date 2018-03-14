import re

from common import file

def get_excerpt(filename):
    content = file.read_file(filename)
    excerpt = content.replace('<p>', '').replace('</p>', '')
    excerpt = re.sub('!\[\]\((.*?)\)', '', excerpt)
    excerpt = re.sub('(\[.+\]\([^\)]+\))', '', excerpt)
    excerpt = re.sub('<.+>', '', excerpt)
    excerpt_list = excerpt.split("\n")
    excerpt_output = ""
    for item in excerpt_list:
        excerpt_output = excerpt_output + item.lstrip("#*-'")
    excerpt = excerpt_output
    if len(excerpt) > 140:
        split_index = 140
        excerpt_output_replace = excerpt_output.replace(".", "。").replace(",", "，")
        dot_index = excerpt_output_replace.find("。", 140, 240)
        comma_index = excerpt_output_replace.find("，", 140, 240)
        if dot_index != -1:
            split_index = dot_index
        if comma_index != -1 and dot_index == 1:
            split_index = comma_index
        excerpt = excerpt_output[:split_index + 1]
    return excerpt

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
