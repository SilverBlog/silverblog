import json
import os

import git

from common import file, console

current_version = 1.4
current_data_version = 1
if os.path.exists("./upgrade/current_version.json"):
    current_data_version = json.loads(file.read_file("./upgrade/current_version.json"))["current_data_version"]
repo = git.Repo("./")
remote = repo.remote()
def fetch_tag():
    remote.fetch("--tags")
    if len(repo.tags) == 0:
        return False
    tags_num = list()
    for item in repo.tags:
        try:
            tags_num.append(float(str(item)))
        except ValueError:
            pass
    return tags_num
def upgrade_check():
    if current_version < max(fetch_tag()):
        return True
    return False
def upgrade_pull():
    console.log("Info", "Current Version is V{}.".format(current_version))
    if repo.is_dirty():
        console.log("Error","The current warehouse is modified and can not be upgraded automatically. Please re-store the warehouse and try again.")
        exit(1)
    remote.pull()
    if not repo.is_dirty() and os.path.exists("./upgrade/upgrade_from_{}.py".format(current_data_version)):
        eval(file.read_file("./upgrade/upgrade_from_{}.py".format(current_data_version)))
    console.log("Success", "Upgrade Successful,Now Version is V{}.".format(max(fetch_tag())))
