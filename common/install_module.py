import importlib


def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        from common import console
        console.log("Error", "Please install the [{}] package to support this feature".format(package))
        install_dependency = input('Do you want to install [{}] now? [y/N]'.format(package))
        if install_dependency.lower() == 'yes' or install_dependency.lower() == 'y':
            try:
                from pip._internal import main
            except Exception:
                from pip import main
            main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)
