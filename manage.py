#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys

from manage import menu

if __name__ == '__main__':
    if len(sys.argv) == 1:
        menu.use_whiptail_mode()
        exit(0)
    parser = argparse.ArgumentParser("SilverBlog CLI tool.")
    parser.add_argument("command", help="The name of the function to execute.")

    #new
    group_new = parser.add_argument_group('new', "Create a new article.")
    group_new.add_argument("-c", "--config", help="The configuration file location you want to load.", type=str)
    group_new.add_argument("-i", "--independent", help="Generate an article that does not appear in the article list",
                           action="store_true")

    parser.add_argument_group('update', "Update article metadata.")

    parser.add_argument_group('theme-install', "Theme pack installation management.")

    parser.add_argument_group('upgrade', "Upgrade program")

    #build-gh-page
    group_build_gh_page = parser.add_argument_group("build-gh-page", "Generate static pages.")
    group_build_gh_page.add_argument("-s", "--static_page", help="Create page that is available to static server",
                                     action="store_true")
    group_build_gh_page.add_argument("-p", "--push_git", help="Automatically submitted to Git", action="store_true")

    args = parser.parse_args()
    
    try:
        menu.use_text_mode(args)
        # After hitting will exit
    except KeyboardInterrupt:
        print("User cancelled operation.")
    parser.print_help()
