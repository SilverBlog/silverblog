print("If the upgrade process fails, please re-upgrade")
print("You can now remove the pypinyin support library")
import os
import time

time.sleep(3)
os.system("cd ./install && bash install_python_dependency.sh && python3 -m pip uninstall pypinyin")
