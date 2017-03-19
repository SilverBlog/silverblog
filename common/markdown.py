import misaka


def markdown(content):
    return misaka.html(content, extensions=misaka.EXT_FENCED_CODE |
                                           misaka.EXT_AUTOLINK | misaka.EXT_TABLES | misaka.EXT_STRIKETHROUGH | misaka.EXT_UNDERLINE)
