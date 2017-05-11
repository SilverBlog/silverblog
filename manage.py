#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json

from common import file
from manage import build_rss, build_static_page, new_post, update_post

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The name of the function to execute.(e.g: new,update,build-gh-page)")
    parser.add_argument("--config", help="The configuration file location you want to load.")
    parser.add_argument("--independent",help="Generate an article that does not appear in the article list",action="store_true")
    parser.add_argument("--static_page",help="Create page that is available to static server",action="store_true")
    args = parser.parse_args()
    if args.command == "new":
        config=None
        if args.config is not None:
            config = json.loads(file.read_file(args.config))
        new_post.new_post_init(config, args.independent)
        build_rss.build_rss()
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
    if args.command == "build-gh-page":
        build_static_page.build(args.static_page)