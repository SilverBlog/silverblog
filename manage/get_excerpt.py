import re

from common import file
from common import markdown


def get_excerpt(filename):
    content = file.read_file(filename)
    filter_excerpt = filter_tags(markdown.markdown(content))
    if len(filter_excerpt) > 140:
        excerpt = filter_excerpt[0:140]
    else:
        excerpt = filter_excerpt
    return excerpt


def filter_tags(html):
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    re_br = re.compile('<br\s*?/?>')
    re_h = re.compile('</?\w+[^>]*>')
    re_comment = re.compile('<!--[^>]*-->')
    s = re_cdata.sub('', html)
    s = re_script.sub('', s)
    s = re_style.sub('', s)
    s = re_br.sub('', s)
    s = re_h.sub('', s)
    s = re_comment.sub('', s)
    blank_line = re.compile('\n+')
    s = blank_line.sub('', s)
    blank_line_l = re.compile('\n')
    s = blank_line_l.sub('', s)
    blank_kon = re.compile('\t')
    s = blank_kon.sub('', s)
    blank_one = re.compile('\r\n')
    s = blank_one.sub('', s)
    blank_two = re.compile('\r')
    s = blank_two.sub('', s)
    blank_three = re.compile(' ')
    s = blank_three.sub('', s)
    return s
