#!/usr/bin/env python3
import os
import sys
import importlib
install_command = ['install', "-U"]
def install():
    try:
        from pip import main as pip_main
    except ImportError:
        from pip._internal import main as pip_main #Loading a pip with version < 10.0.0
    if os.geteuid() != 0:
        print("The current user is not root and is installed in user mode.")
        install_command.append("--user")
    if sys.version_info < (3, 4):
        print("Current python version is lower than 3.4, need to install asyncio.")
        install_command.append("asyncio")

    test_install("qrcode_terminal","Do you want to install [qrcode_terminal] to support QR code login?")
    test_install("xpinyin","Do you want to install [xpinyin] to support pinyin slug?")
    install_command.extend(["Flask", "hoedown", "pyrss2gen", "gitpython", "requests", "watchdog"])
    pip_main(install_command)

def test_install(name,question):
    try:
        importlib.import_module(name)
    except ImportError:
        install_dependency = "n"
        try:
            install_dependency = str(input( "(y/N)").format(question))
        except EOFError:
            print("N")
        if install_dependency.lower() == 'y':
            global install_command
            install_command.append(name)

def main():
    install()

if __name__ == '__main__':
    install()
