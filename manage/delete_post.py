import json
import os
import shutil

from common import file

def delete(page_list, post_index):
    file_name = page_list[post_index]["name"]
    del page_list[post_index]
    file.write_file("./config/page.json", json.dumps(page_list, indent=4, sort_keys=False, ensure_ascii=False))
    if not os.path.exists("./trash"):
        os.mkdir("./trash")
    if os.path.exists("./trash/{0}.md".format(file_name)):
        os.remove("./trash/{0}.md".format(file_name))
    shutil.move("./document/{0}.md".format(file_name), "./trash/{0}.md".format(file_name))
