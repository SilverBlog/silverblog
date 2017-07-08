import json
import os
import shutil


def build(github_mode):
    from common import file, page, console
    html_static = False
    if github_mode is not None:
        html_static = github_mode
    page_list = json.loads(file.read_file("./config/page.json"))
    menu_list = json.loads(file.read_file("./config/menu.json"))
    system_config = json.loads(file.read_file("./config/system.json"))
    template_config = None
    if os.path.exists("./templates/{0}/config.json".format(system_config["Theme"])):
        template_config = json.loads(file.read_file("./templates/{0}/config.json".format(system_config["Theme"])))

    if os.path.isdir("./static_page"):
        shutil.rmtree("./static_page")
    os.mkdir("./static_page")
    page_name_list = list()
    for item in page_list:
        page_name_list.append(item["name"])
    console.log("Build", "Processing file: ./static_page/index.html")
    content, row = page.build_index(1, system_config, page_list, menu_list, html_static, template_config)
    file.write_file("./static_page/index.html", content)
    if row != 1:
        os.mkdir("./static_page/index/")
        os.mkdir("./static_page/index/p")
        file.write_file("./static_page/index/p/1.html", "<meta http-equiv='refresh' content='0.1; url=/'>")
        for page_id in range(2, row + 1):
            console.log("Build", "Processing file: ./static_page/index/p/{0}.html".format(str(page_id)))
            content, row = page.build_index(page_id, system_config, page_list, menu_list, html_static, template_config)
            file.write_file("./static_page/index/p/{0}.html".format(str(page_id)), content)
    for filename in os.listdir("./document/"):
        if filename.endswith(".md"):
            console.log("Build", "Processing file: ./static_page/{0}.html".format(filename.replace(".md", "")))
            content = page.build_page(filename.replace(".md", ""), system_config, page_list, page_name_list, menu_list,
                                      html_static, template_config)
            if content is not None:
                file.write_file("./static_page/{0}.html".format(filename.replace(".md", "")), content)
    shutil.copyfile("./document/rss.xml", "./static_page/rss.xml")
    shutil.copytree("./templates/static/{0}/".format(system_config["Theme"]),
                    "./static_page/static/{0}/".format(system_config["Theme"]))
    shutil.copytree("./templates/static/user_file",
                    "./static_page/static/user_file")
    console.log("Success", "Create Github Page Success!")
