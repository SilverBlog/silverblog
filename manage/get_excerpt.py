import re

from common import file

def get_excerpt(filename):
    content = file.read_file(filename)
    excerpt = content.replace('<p>', '').replace('</p>', '')
    excerpt = re.sub('!\[\]\((.*?)\)', '', excerpt)
    excerpt_list = excerpt.split("\n")
    excerpt_output = ""
    for item in excerpt_list:
        excerpt_output = excerpt_output + item.lstrip("#*-'")
    if len(excerpt_output) > 140:
        excerpt = excerpt_output[:140]
    return excerpt