#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

print("Current python version information:")
print(sys.version)
if sys.version_info < (3, 4):
    print("Current python version is lower than 3.4, need to install asyncio.")
    os.system("python3 -m pip install asyncio")
