#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import json

from common import file, console
from manage import build_rss, build_static_page, new_post, update_post, theme

if __name__ == '__main__':
    parser = argparse.ArgumentParser("SilverBlog command line management tool.")
    parser.add_argument("command",
                        help="The name of the function to execute.")

    #new
    group_new = parser.add_argument_group('new', "Create a new article.")
    group_new.add_argument("--config", help="The configuration file location you want to load.")
    group_new.add_argument("--independent", help="Generate an article that does not appear in the article list",
                           action="store_true")
    group_new = parser.add_argument_group('update', "Update article metadata.")
    #theme
    group_theme = parser.add_argument_group('theme', "Theme pack installation management.")
    group_theme.add_argument("--list",action="store_true")
    group_theme.add_argument("--install",action="store_true")
    #build-gh-page
    group_build_gh_page = parser.add_argument_group("build-gh-page", "Generate static pages.")
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
            title = input()
            print("Please enter the URL (Leave a blank use pinyin):")
            name = input()
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
    if args.command == "Upgrade":
        from manage import upgrade

        if upgrade.upgrade_check():
            start_to_pull = input('Find new version, do you want to upgrade? [y/N]')
            if start_to_pull.lower() == 'yes' or start_to_pull.lower() == 'y':
                upgrade.upgrade_pull()
                exit(0)
        console.log("No upgrade found")
    if args.command == "theme":
        if args.list:
            req = theme.get_orgs_list()
            for item in req:
                print("-" * 100)
                print(
                    " Name:{0}\n Description:{1}\n Star:{2}".format(item["name"], item["description"],
                                                                    item["stargazers_count"]))
                print("-" * 100)
        if args.install:
            print("Please enter the name of the theme you want to install:")
            theme_name = input()
            theme_name = theme.install_theme(theme_name)
            enable_theme = input('Do you want to enable this theme now? [y/N]')
            if enable_theme.lower() == 'yes' or enable_theme.lower() == 'y':
                theme.set_theme(theme_name)
        exit(0)
    if args.command == "build-gh-page":
        build_static_page.publish(args.push_git, args.static_page)
        exit(0)
