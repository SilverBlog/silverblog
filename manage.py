#!/usr/bin/env python3

import argparse
import json
import os
import sys

from common import file, console

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
                console.log("Error", "Please install docker or upgrade the current docker image and try again.")
            exit(result_code)
if __name__ == '__main__':
    if not os.path.exists("./config/page.json") or not os.path.exists("./config/menu.json"):
        console.log("Error", "Please execute the installation wizard first.")
        exit(1)
    if not os.path.exists("./config/system.json"):
        from manage import setting

        setting.setup_wizard()
        setting.theme_manage()
        exit(0)

    if len(sys.argv) == 1:
        from manage import menu
        menu.use_whiptail_mode()
        exit(0)
    parser = argparse.ArgumentParser("SilverBlog management tool")
    parser.add_argument("command", help="The name of the function to execute.", )

    #new
    new_parser = parser.add_argument_group('new', "Create a new article.")
    new_parser.add_argument("-c", "--config", help="The configuration file location you want to load.", type=str)
    new_parser.add_argument("-i", "--independent", help="Generate an article that does not appear in the article list.",
                            action="store_true")

    parser.add_argument_group('update', "Update article metadata.")

    upgrade_parser = parser.add_argument_group('upgrade', "Upgrade program.")
    upgrade_parser.add_argument("-y", "--yes", help="Assume yes for all questions, do not ask.", action="store_true")
    parser.add_argument_group('setting', "Setting program.")
    parser.add_argument_group('qrcode', "Output client qrcode.")
    #build-gh-page
    parser.add_argument_group("build-page", "Generate static pages.")
    theme_group = parser.add_argument_group("install_theme")
    theme_group.add_argument("--name", help="Install the theme in the official repository.", type=str)
    theme_group.add_argument("--custom", help="Install the theme of the custom repository.", type=str)
    parser.add_argument_group("backup", "Back up the current data.")
    args = parser.parse_args()
    try:
        if args.command == "setting":
            from manage import setting

            setting.setting_menu(True)
            exit(0)

        if args.command == "qrcode":
            from common import install_module

            install_module.install_and_import("qrcode_terminal")
            import qrcode_terminal

            control_config = json.loads(file.read_file("./config/control.json"))

            if len(control_config["password"]) == 0 or len(system_config["Project_URL"]) == 0:
                console.log("Error", "Check the API_Password and Project_URL configuration items")
                exit(1)
            password = control_config["password"]
            console.log("Info", "Please use the client to scan the following QR Code")
            url = system_config["Project_URL"].replace("https://", "").replace("http://", "")
            config_json = json.dumps({"H": url, "P": password})
            qrcode_terminal.draw(config_json)
            exit(0)

        if args.command == "upgrade":
            from manage import upgrade

            is_git = False
            if upgrade.check_is_git():
                if upgrade.upgrade_check():
                    if not args.yes:
                        start_to_pull = input('Find new version, do you want to upgrade? [y/N]')
                    if start_to_pull.lower() == 'yes' or start_to_pull.lower() == 'y' or args.yes:
                        upgrade.upgrade_pull()
                is_git = True
            if not is_git:
                console.log("Info", "No upgrade found")
            upgrade.upgrade_env()
            upgrade.upgrade_data()
            exit(0)

        if args.command == "backup":
            from manage import backup

            backup.backup()
            exit(0)

        if args.command == "install_theme":
            custom = False
            name = args.name
            if args.custom is not None:
                custom = True
                name = args.custom
            from manage import theme
            theme.install_theme(name, custom)
            exit(0)


        if args.command == "build-page":
            from manage import build_static_page
            build_static_page.publish()
            exit(0)

        from manage import build_rss, post_manage, get
        if args.command == "new":
            config = None
            if args.config is not None:
                config = json.loads(file.read_file(args.config))
            if config is None:
                print("Please enter the title of the article:")
                title = input().strip()
                if len(title) == 0:
                    console.log("Error", "The title can not be blank.")
                    exit(1)
                name = get.get_name(title, system_config["Pinyin"])
                print("Please enter the slug [{}]:".format(name))
                name2 = input().strip()
                if len(name2) != 0:
                    name = get.filter_name(name2)
                if os.path.exists("./document/{}.md".format(name)):
                    console.log("Error", "File [./document/{}.md] already exists".format(name))
                    exit(1)
            if len(name) != 0 and len(title) != 0:
                config = {"title": title, "name": name}
                post_manage.new_post(config, args.independent)
                build_rss.build_rss()
            exit(0)

        if args.command == "update":
            if post_manage.update_post():
                build_rss.build_rss()
            exit(0)

    except KeyboardInterrupt:
        print("User cancelled operation.")
        exit(0)
    parser.print_help()