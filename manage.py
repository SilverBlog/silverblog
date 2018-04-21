#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys

from manage import menu

sys.setdefaultencoding("utf-8")
if __name__ == '__main__':
    if len(sys.argv) == 1:
        menu.use_whiptail_mode()
        exit(0)
    parser = argparse.ArgumentParser("SilverBlog management tool")
    parser.add_argument("command", help="The name of the function to execute.", )

    #new
    group_new = parser.add_argument_group('new', "Create a new article.")
    group_new.add_argument("-c", "--config", help="The configuration file location you want to load.", type=str)
    group_new.add_argument("-i", "--independent", help="Generate an article that does not appear in the article list",
                           action="store_true")

    parser.add_argument_group('update', "Update article metadata.")

    parser.add_argument_group('upgrade', "Upgrade program")
    parser.add_argument_group('setting', "Setting program")
    parser.add_argument_group('qrcode', "Output client qrcode.")
    #build-gh-page
    group_build_gh_page = parser.add_argument_group("build-page", "Generate static pages.")

    args = parser.parse_args()
    if args.command == "setting":
        from manage import setting
        setting.setup_wizard()
        exit(0)
    try:
        menu.use_text_mode(args)
        # After hitting will exit
    except KeyboardInterrupt:
        print("User cancelled operation.")
        exit(0)
    parser.print_help()
