#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import argparse
import json

from common import file
from manage import build_rss, build_static_page, new_post, update_post

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The name of the function to execute.(e.g: new,update,build-gh-page)")
    parser.add_argument("--config", help="The configuration file location you want to load.")
    parser.add_argument("--independent", help="Generate an article that does not appear in the article list",
                        action="store_true")
    parser.add_argument("--static_page", help="Create page that is available to static server", action="store_true")
    parser.add_argument("--push_git", help="Automatically submitted to Git", action="store_true")
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
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
    if args.command == "build-gh-page":
        if args.push_git:
            from manage import git_publish
            git_publish.git_publish(args.static_page)
            exit(0)
        build_static_page.build(args.static_page)
