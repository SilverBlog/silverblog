#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

from manage import build_rss
from manage import build_static_page
from manage import new_post
from manage import update_post

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The name of the function to execute.(e.g: new,update,build-rss,build-gh-page)")
    parser.add_argument("--config", help="The configuration file location you want to load.")
    parser.add_argument("--editor", help="Your favorite editor(e.g: vim,nano,gedit,vi)")
    args = parser.parse_args()
    if args.command == "new":
        if args.editor is not None:
            new_post.new_post_init(args.config, args.editor)
        else:
            new_post.new_post_init(args.config)
        build_rss.build_rss()
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
    if args.command == "build-rss":
        build_rss.build_rss()
    if args.command == "build-gh-page":
        build_rss.build_rss()
        build_static_page.build()
