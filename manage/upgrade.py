import json
import os

import git

from common import file, console

new_data_version = 2
if not os.path.exists("./upgrade/current_version.json"):
    file.write_file("./upgrade/current_version.json", json.dumps({"current_data_version": new_data_version}))
current_data_version = json.loads(file.read_file("./upgrade/current_version.json"))["current_data_version"]
if not os.path.exists("./.git"):
    console.log("Error", "Not a git repository.")
repo = git.Repo("./")
remote = repo.remote()
def upgrade_check():
    remote.fetch(repo.active_branch)
    if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD") or current_data_version != new_data_version:
        return True
    return False
def upgrade_pull():
    if repo.is_dirty():
        console.log("Error",
                    "The current warehouse is modified and can not be upgraded automatically. Please re-store the warehouse and try again.")
        exit(1)
    remote.pull()
    os.system("python3 -m pip install -r ./install/python_dependency.txt")
    if os.path.exists("./upgrade/upgrade_from_{}.py".format(current_data_version)):
        exec(file.read_file("./upgrade/upgrade_from_{}.py".format(current_data_version)))
        file.write_file("./upgrade/current_version.json", json.dumps({"current_data_version": new_data_version}))
    console.log("Success", "Upgrade Successful!")
    console.log("Info", "Please restart your service process to ensure that the program is up and running.")
    exit(0)
