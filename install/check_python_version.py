#!/usr/bin/env python3

import sys

print("Current python version information:")
print(sys.version)
if sys.version_info < (3, 4):
    print("Current python version is lower than 3.4, need to install asyncio.")
    from common import install_module

    install_module.install_and_import("asyncio")
