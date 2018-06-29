import re

from xpinyin import Pinyin

from common import file, console


def get_name(name_input):
    p = Pinyin()
    name = name_input.replace(" ", "-").replace("。", ".").replace("，", ",")
    name = filter_name(re.sub('[/:*?,.<>|\'"\\\]', '', name))
    return p.get_pinyin(name)

def get_excerpt(filename):
    content = file.read_file(filename)
    excerpt_output = re.sub('<[\\s\\S]*?>[\\s\\S]*?<[\\s\\S]*?>|<[\\s\\S]*?/>', '', content)
    excerpt_output = re.sub('(!\[.*\]\([^)]*\))', '', excerpt_output)
    excerpt_output = re.sub('\[(.*)\].*(\(.*/.*\))', '\g<1>', excerpt_output)
    excerpt_output = re.sub('\*+|`|#+|>+|~+|=+|-+|_', '', excerpt_output)
    excerpt = excerpt_output.replace("\n", "").strip()
    if len(excerpt) > 140:
        split_index = 140
        excerpt_output_replace = excerpt_output.replace("。", ".").replace("，", ",")
        newline_index = excerpt_output_replace.find("\n", 140, 340)
        dot_index = excerpt_output_replace.find(".", 140, 340)
        comma_index = excerpt_output_replace.find(",", 140, 340)
        if newline_index != -1:
            split_index = newline_index
        if newline_index == -1 and dot_index != -1:
            split_index = dot_index - 1
        if dot_index == -1 and comma_index != -1:
            split_index = comma_index - 1
        excerpt = excerpt_output[:split_index].replace("\n", "").strip()
    return excerpt

def get_gravatar(author_name):
    import requests
    console.log("info", "Get Gravatar URL...")
    gravatar_hash = ""
    try:
        r = requests.get("https://en.gravatar.com/{0}.json".format(author_name)).json()
        gravatar_hash = r["entry"][0]["hash"]
        console.log("Success", "Get Gravatar URL success.")
    except (TypeError, ValueError, requests.exceptions.RequestException):
        console.log("Error", "Get Gravatar URL error,use default avatar.")
    return "https://secure.gravatar.com/avatar/{0}".format(gravatar_hash)


def filter_name(name):
    sub = re.sub('[/:*?<>|\'"\\\]', '', name)
    sub = sub.replace(".", "")
    return sub
