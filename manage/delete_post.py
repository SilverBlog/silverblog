import os
import shutil

from common import file


def delete(page_list, post_index):
    file_name = page_list[post_index]["name"]
    meta_backup = page_list[post_index]
    del page_list[post_index]
    file.write_file("./config/page.json", file.json_format_dump(page_list))
    if not os.path.exists("./trash"):
        os.mkdir("./trash")
    check_file("{}.md".format(file_name))
    check_file("{}.json".format(file_name))
    file.write_file("./trash/{}.json".format(file_name), file.json_format_dump(meta_backup))
    shutil.move("./document/{}.md".format(file_name), "./trash/{}.md".format(file_name))

def check_file(file_name):
    if os.path.exists("./trash/{}".format(file_name)):
        os.remove("./trash/{}".format(file_name))