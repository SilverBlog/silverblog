#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

from common import file
from manage import build_rss, build_static_page, new_post, update_post

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The name of the function to execute.(e.g: new,update,build-rss,build-gh-page,build-static-page)")
    parser.add_argument("--config", help="The configuration file location you want to load.")
    parser.add_argument("--editor", help="Your favorite editor(e.g: vim,nano,gedit)")
    args = parser.parse_args()
    if args.command == "new":
        config=None
        if args.config is not None:
            config=file.read_file(args.config)
        new_post.new_post_init(config, args.editor)
        build_rss.build_rss()
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
    if args.command == "build-rss":
        build_rss.build_rss()
    if args.command == "build-gh-page":
        build_rss.build_rss()
        build_static_page.build(False)
    if args.command == "build-static-page":
        build_rss.build_rss()
        build_static_page.build(True)
