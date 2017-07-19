import os.path
import shutil
import time

import git

localtime = time.asctime(time.localtime(time.time()))

from manage import build_static_page


def git_publish():
    if not os.path.exists("./static_page/.git"):
        return False
    if not os.path.exists("./.temp"):
        os.mkdir("./.temp")
    shutil.copytree("./static_page/.git", "./.temp/.git")
    build_static_page.build(True)
    shutil.copytree("./.temp/.git", "./static_page/.git")
    shutil.rmtree("./.temp/.git")
    repo = git.Repo("./static_page")
    repo.git.add('--all')
    repo.commit("Publish Time：{0}".format(localtime))
    remote = repo.remote()
    remote.push()
