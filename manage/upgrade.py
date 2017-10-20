import json
import os

import git

from common import file, console

current_data_version = 1
if os.path.exists("./upgrade/current_version.json"):
    current_data_version = json.loads(file.read_file("./upgrade/current_version.json"))["current_data_version"]
repo = git.Repo("./")
remote = repo.remote()
def upgrade_check():
    info = remote.fetch("master")
    if info[0] != "FETCH_HEAD":
        return True
    return False
def upgrade_pull():
    if repo.is_dirty():
        console.log("Error","The current warehouse is modified and can not be upgraded automatically. Please re-store the warehouse and try again.")
        exit(1)
    remote.pull()
    if not repo.is_dirty() and os.path.exists("./upgrade/upgrade_from_{}.py".format(current_data_version)):
        eval(file.read_file("./upgrade/upgrade_from_{}.py".format(current_data_version)))
    console.log("Success", "Upgrade Successful!")
    console.log("Info", "Please restart your service process to ensure that the program is up and running.")
    exit(0)
