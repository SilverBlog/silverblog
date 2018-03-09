print("If the upgrade process fails, please re-upgrade")
print("You can now remove the pypinyin support library")
import os

os.system("cd ./install && bash install_python_dependency.sh")
uninstall_dependency = input('Do you want to enable this theme now? [y/N]')
if uninstall_dependency.lower() == 'yes' or uninstall_dependency.lower() == 'y':
    os.system("sudo python3 -m pip uninstall pypinyin")
print("We modified the startup script, please redeploy the startup script.")