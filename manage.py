#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import json

from common import file
from manage import build_rss, build_static_page, new_post, update_post, theme

if __name__ == '__main__':
    parser = argparse.ArgumentParser("SilverBlog command line management tool.")
    parser.add_argument("command",
                        help="The name of the function to execute.(e.g: new,update,build-gh-page,theme,tools)")
    #new
    group_new = parser.add_argument_group('new')
    group_new.add_argument("--config", help="The configuration file location you want to load.")
    group_new.add_argument("--independent", help="Generate an article that does not appear in the article list",
                           action="store_true")
    #theme
    group_theme = parser.add_argument_group('theme')
    group_theme.add_argument("--list",action="store_true")
    group_theme.add_argument("--install",action="store_true")
    #build-gh-page
    group_build_gh_page = parser.add_argument_group("build-gh-page")
    group_build_gh_page.add_argument("--static_page", help="Create page that is available to static server",
                                     action="store_true")
    group_build_gh_page.add_argument("--push_git", help="Automatically submitted to Git", action="store_true")
    args = parser.parse_args()
    if args.command == "new":
        config = None
        if args.config is not None:
            config = json.loads(file.read_file(args.config))
        if config is None:
            print("Please enter the title of the article:")
            title = raw_input()
            print("Please enter the URL (Leave a blank use pinyin):")
            name = raw_input()
            if len(name) == 0:
                name = new_post.get_name(title)
            config = {"title": title, "name": name}
        new_post.new_post_init(config, args.independent)
        build_rss.build_rss()
        exit(0)
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
        exit(0)
    if args.command == "theme":
        if args.list:
            theme.get_theme_list()
        if args.install:
            print("Please enter the name of the theme you want to install:")
            theme_name = raw_input()
            theme.install_theme(theme_name)
        exit(0)
    if args.command == "build-gh-page":
        build_static_page.publish(args.push_git, args.static_page)
        exit(0)
