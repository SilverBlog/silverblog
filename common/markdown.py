import hoedown

def markdown(content, skip_html=False):
    render_flags = 0
    if skip_html:
        render_flags = hoedown.HTML_SKIP_HTML
    return hoedown.html(content, extensions=hoedown.EXT_FENCED_CODE | hoedown.EXT_HIGHLIGHT |
                                            hoedown.EXT_AUTOLINK | hoedown.EXT_TABLES | hoedown.EXT_STRIKETHROUGH | hoedown.EXT_UNDERLINE,
                        render_flags=render_flags)
