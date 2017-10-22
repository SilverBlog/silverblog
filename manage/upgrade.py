import json
import os

import git

from common import file, console

current_data_version = 1
new_data_version = 2
if os.path.exists("./upgrade/current_version.json"):
    current_data_version = json.loads(file.read_file("./upgrade/current_version.json"))["current_data_version"]
repo = git.Repo("./")
remote = repo.remote()
def upgrade_check():
    if remote.fetch("master")[0] == "FETCH_HEAD":
        return True
    if current_data_version != new_data_version:
        return True
    return True
def upgrade_pull():
    if repo.is_dirty():
        console.log("Error","The current warehouse is modified and can not be upgraded automatically. Please re-store the warehouse and try again.")
        exit(1)
    remote.pull()
    if not repo.is_dirty() and os.path.exists("./upgrade/upgrade_from_{}.py".format(current_data_version)):
        exec(file.read_file("./upgrade/upgrade_from_{}.py".format(current_data_version)))
        data_version = dict()
        data_version["current_data_version"] = new_data_version
        file.write_file("./upgrade/current_version.json", json.dumps(data_version))
    console.log("Success", "Upgrade Successful!")
    console.log("Info", "Please restart your service process to ensure that the program is up and running.")
    exit(0)
