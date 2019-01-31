import os
import tarfile
import time

from common import console


def backup(version=None):
    console.log("Info", "The data is being backed up...")
    if not os.path.exists("./backup"):
        os.mkdir("./backup")
    file_name = "./backup/backup-{}.tar.gz".format(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    if version is not None:
        file_name = "./backup/backup-version_{}-{}.tar.gz".format(version,
                                                                  time.strftime("%Y%m%d%H%M%S", time.localtime()))
    console.log("Info", "Write the file: {0}".format(file_name))
    tar = tarfile.open(file_name, "w:gz")
    add_tar_file(tar, "./config")
    add_tar_file(tar, "./document")
    add_tar_file(tar, "./templates")
    add_tar_file(tar, "./static_page")
    tar.close()
    console.log("Success", "The backup is complete.")


def add_tar_file(tar, dir_name):
    for root, path, files in os.walk(dir_name):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath)
