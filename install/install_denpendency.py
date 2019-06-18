#!/usr/bin/env python3
import os
import sys
import importlib

def install():
    try:
        from pip import main as pip_main
    except ImportError:
        from pip._internal import main as pip_main
    install_command = ['install', "-U"]
    if os.geteuid() != 0:
        print("The current user is not root and is installed in user mode.")
        install_command.append("--user")
    if sys.version_info < (3, 4):
        print("Current python version is lower than 3.4, need to install asyncio.")
        install_command.append("asyncio")
    try:
        importlib.import_module("qrcode_terminal")
    except ImportError:
        install_qrcode_dependency = "n"
        try:
            install_qrcode_dependency = str(input("Do you want to install [qrcode_terminal] to support QR code login? (y/N)"))
        except EOFError:
            print("N")
        if install_qrcode_dependency.lower() == 'y':
            install_command.append("qrcode_terminal")
    install_command.extend(["Flask", "hoedown", "xpinyin", "pyrss2gen", "gitpython", "requests", "watchdog"])
    pip_main(install_command)



if __name__ == '__main__':
    install()
