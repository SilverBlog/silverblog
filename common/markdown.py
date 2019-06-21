import hoedown


class image_renderer(hoedown.HtmlRenderer):
    def image(self, src, title, alt):
        param = ""
        if title is not None:
            param = " title=\"{}\"".format(title)
        if alt is not None:
            param = param + "alt=\"{}\"".format(alt)
        return "<img src=\"{}\" lazyload=\"on\"{}>".format(src, param)


def markdown(system_config, content):
    renderer = hoedown.HtmlRenderer()
    if 'Lazyload' in system_config and system_config['Lazyload']:
        renderer = image_renderer()
    md = hoedown.Markdown(renderer, extensions=hoedown.EXT_FENCED_CODE | hoedown.EXT_HIGHLIGHT |
                                               hoedown.EXT_AUTOLINK | hoedown.EXT_TABLES | hoedown.EXT_STRIKETHROUGH | hoedown.EXT_UNDERLINE).render
    return md(content)
