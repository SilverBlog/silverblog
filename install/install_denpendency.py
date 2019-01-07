#!/usr/bin/env python3
import os
import sys


def main():
    try:
        from pip._internal import main
    except Exception:
        from pip import main
    install_command = ['install', "-U"]
    if os.geteuid() != 0:
        print("The current user is not root and is installed in user mode.")
        install_command.append("--user")
    if sys.version_info < (3, 4):
        print("Current python version is lower than 3.4, need to install asyncio.")
        install_command.append("asyncio")
    install_command.extend(["Flask", "hoedown", "xpinyin", "pyrss2gen", "gitpython", "requests", "watchdog"])
    main(install_command)


if __name__ == '__main__':
    main()
