import hoedown

class image_renderer(hoedown.HtmlRenderer):
    def image(self, src, title, alt):
        return "<img src=\"{}\" alt=\"{}\" title=\"{}\" lazyload=\"on\">".format(src,alt,title)


def markdown(system_config,content):
    renderer = hoedown.HtmlRenderer()
    if 'Lazyload' in system_config and system_config['Lazyload']:
        renderer = image_renderer()
    md = hoedown.Markdown(renderer,extensions=hoedown.EXT_FENCED_CODE | hoedown.EXT_HIGHLIGHT |
                                            hoedown.EXT_AUTOLINK | hoedown.EXT_TABLES  | hoedown.EXT_STRIKETHROUGH | hoedown.EXT_UNDERLINE).render
    return md(content)