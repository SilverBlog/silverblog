#!/usr/bin/env python3

import argparse
import json
import os
import sys

from common import file

if os.path.exists("./install/install.lock"):
    if json.loads(file.read_file("./install/install.lock"))["install"] == "docker" and not os.environ.get(
            'DOCKER_CONTAINER', False):
            args = ""
            for arg in sys.argv[1:]:
                args = args + " " + arg
            result_code = os.system(
                "docker run -it --rm -v {0}:/home/silverblog silverblog/silverblog ./manage.py{1}".format(
                os.getcwd(), args))
            if (result_code >> 8) == 127:
                print("Please install docker or upgrade the current docker image and try again.")
            exit(result_code)
if __name__ == '__main__':
    from manage import menu
    if not os.path.exists("./config/page.json") or not os.path.exists("./config/menu.json"):
        print("Please execute the installation wizard first.")
        exit(1)
    if not os.path.exists("./config/system.json"):
        from manage import setting

        setting.setup_wizard()
        setting.theme_manage()
        exit(0)

    if len(sys.argv) == 1:
        menu.use_whiptail_mode()
        exit(0)
    parser = argparse.ArgumentParser("SilverBlog management tool")
    parser.add_argument("command", help="The name of the function to execute.", )

    #new
    new_parser = parser.add_argument_group('new', "Create a new article.")
    new_parser.add_argument("-c", "--config", help="The configuration file location you want to load.", type=str)
    new_parser.add_argument("-i", "--independent", help="Generate an article that does not appear in the article list",
                            action="store_true")

    parser.add_argument_group('update', "Update article metadata.")

    upgrade_parser = parser.add_argument_group('upgrade', "Upgrade program")
    upgrade_parser.add_argument("-y", "--yes", help="Assume yes for all questions, do not ask.", action="store_true")
    parser.add_argument_group('setting', "Setting program")
    parser.add_argument_group('qrcode', "Output client qrcode.")
    #build-gh-page
    group_build_gh_page = parser.add_argument_group("build-page", "Generate static pages.")

    args = parser.parse_args()
    if args.command == "setting":
        from manage import setting

        setting.setting_menu(True)
        exit(0)
    try:
        menu.use_text_mode(args)
        # After hitting will exit
    except KeyboardInterrupt:
        print("User cancelled operation.")
        exit(0)
    parser.print_help()
