import os.path
import shutil
import time

import git

localtime = time.asctime(time.localtime(time.time()))

from manage import build_static_page
from common import console


def git_publish(static):
    if not os.path.exists("./static_page/.git"):
        return False
    if not os.path.exists("./.temp"):
        os.mkdir("./.temp")
    shutil.copytree("./static_page/.git", "./.temp/.git")
    build_static_page.build(static)
    shutil.copytree("./.temp/.git", "./static_page/.git")
    shutil.rmtree("./.temp/.git")
    repo = git.Repo("./static_page")
    repo.git.add("--all")
    try:
        repo.git.commit("-m \"Publish Time：{0}\"".format(localtime))
    except git.exc.GitCommandError as e:
        console.log("Error", e.args)
        return False
    console.log("Info", "Submitted to the remote")
    remote = repo.remote()
    remote.push()
    console.log("Success", "Done")
    return True
