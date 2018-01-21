import re

from common import file, markdown

def get_excerpt(filename):
    content = file.read_file(filename)
    excerpt = filter_tags(markdown.markdown(content, True))
    if len(excerpt) > 140:
        excerpt = excerpt[0:140]
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
    return s
