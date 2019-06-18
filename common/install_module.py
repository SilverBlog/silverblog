import importlib
import os

from common import console


def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        console.log("Error", "Please install the [{}] package to support this feature".format(package))
        install_dependency = input('Do you want to install [{}] now? [y/N]'.format(package))
        if install_dependency.lower() == 'yes' or install_dependency.lower() == 'y':
            install_package(package)
    finally:
        globals()[package] = importlib.import_module(package, __package__)


def install_package(package):
    from pip import main
    install_command = ['install']
    if os.geteuid() != 0:
        install_command.append("--user")
    install_command.append(package)
    main(install_command)


def uninstall_package(package):

    from pip import main
    install_command = ['uninstall']
    if os.geteuid() != 0:
        install_command.append("--user")
    install_command.append(package)
    main(install_command)
