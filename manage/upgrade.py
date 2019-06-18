import importlib
import json
import os

import git

from common import file, console

new_data_version = 4
current_data_version = new_data_version
if not os.path.exists("./upgrade/current_version.json"):
    file.write_file("./upgrade/current_version.json",
                    json.dumps({"current_data_version": new_data_version}))
current_version_json = json.loads(file.read_file("./upgrade/current_version.json"))
current_data_version = current_version_json["current_data_version"]



def check_is_git():
    if os.system('git rev-parse 2> /dev/null > /dev/null') == 0:
        return True
    return False

def upgrade_check(fetch=True):
    if not check_is_git():
        if fetch:
            console.log("Error", "Not a git repository.")
            exit(1)
        return False
    repo = git.Repo("./")
    remote = repo.remote()
    if fetch:
        remote.fetch(repo.active_branch)
        try:
            if repo.rev_parse("HEAD") != repo.rev_parse("FETCH_HEAD"):
                return True
        except git.BadObject:
            pass
        if current_data_version != new_data_version:
            return True
    return False

def upgrade_pull():
    if not check_is_git():
        console.log("Error", "Not a git repository.")
        return False
    repo = git.Repo("./")
    remote = repo.remote()
    console.log("Info", "Current upgrade channel: {}".format(repo.active_branch))
    if repo.is_dirty():
        console.log("Error", "The current warehouse is modified and can not be upgraded automatically.")
        exit(1)
    remote.pull()
    console.log("Success", "Upgrade code Successful!")

def upgrade_env():
    from install import install_denpendency
    install_denpendency.main()
    console.log("Success", "Upgrade env Successful!")

def upgrade_data():
    if current_data_version != new_data_version:
        from manage import backup
        backup.backup(str(current_data_version))
        for index in range(current_data_version, new_data_version):
            if os.path.exists("./upgrade/upgrade_from_{}.py".format(index)):
                upgrade_item = importlib.import_module("upgrade.upgrade_from_{}".format(index), __package__)
                upgrade_item.main()
        file.write_file("./upgrade/current_version.json",
                        json.dumps({"current_data_version": new_data_version}))
        console.log("Success", "Upgrade data Successful!")
