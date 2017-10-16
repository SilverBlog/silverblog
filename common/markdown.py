import hoedown


def markdown(content):
    return hoedown.html(content, extensions=hoedown.EXT_FENCED_CODE | hoedown.EXT_HIGHLIGHT |
                                            hoedown.EXT_AUTOLINK | hoedown.EXT_TABLES | hoedown.EXT_STRIKETHROUGH | hoedown.EXT_UNDERLINE)
