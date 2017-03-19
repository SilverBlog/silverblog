import json
import os
import shutil

from common import file
from common import page


def build():
    page_list = json.loads(file.read_file("./config/page.json"))
    menu_list = json.loads(file.read_file("./config/menu.json"))
    system_config = json.loads(file.read_file("./config/system.json"))
    if os.path.isdir("./static_page"):
        shutil.rmtree("./static_page")
    os.mkdir("./static_page")
    page_name_list = list()
    for item in page_list:
        page_name_list.append(item["name"])
    content, row = page.build_index(1, system_config, page_list, menu_list, True)
    file.write_file("./static_page/index.html", content)
    if row != 1:
        file.write_file("./static_page/index_1.html", "<meta http-equiv='refresh' content='0.1; url=/'>")
        for page_id in range(2, row + 1):
            content, row = page.build_index(page_id, system_config, page_list, menu_list, True)
            file.write_file("./static_page/index_{0}.html".format(str(page_id)), content)
    for filename in os.listdir("./document/"):
        if filename.endswith(".md"):
            content = page.build_page(filename.replace(".md", ""), system_config, page_list, page_name_list, menu_list,
                                      True)
            if content is not None:
                file.write_file("./static_page/{0}.html".format(filename.replace(".md", "")), content)
    shutil.copyfile("./document/rss.xml", "./static_page/rss.xml")
    shutil.copytree("./templates/static/{0}/".format(system_config["Theme"]),
                    "./static_page/static/{0}/".format(system_config["Theme"]))
    shutil.copytree("./templates/static/user_file",
                    "./static_page/static/user_file")
    print("Build Github Pages Success!")
