print("If the upgrade process fails, please re-upgrade")
print("You can now remove the pypinyin support library")
import os
os.system("cd ./install && bash install_python_dependency.sh && sudo python3 -m pip uninstall pypinyin")
print("We modified the startup script, please redeploy the startup script.")
