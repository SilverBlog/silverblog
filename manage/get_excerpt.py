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
    if len(excerpt_output) > 140:
        split_index = 140
        excerpt_output_replace = excerpt_output.replace(".", "。").replace(",", "，")
        dot_index = excerpt_output_replace.find("。", 140, 240)
        comma_index = excerpt_output_replace.find("，", 140, 240)
        if dot_index != -1:
            split_index = dot_index
        if comma_index != -1 and dot_index == 1:
            split_index = comma_index
        excerpt = excerpt_output[:split_index]
    return excerpt