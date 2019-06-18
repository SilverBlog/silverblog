if __name__ == '__main__':
    print("The upgrade script has changed. You need to execute the upgrade command again to update the data structure.")
    exit(0)

import json
import os
import shutil
from common import file


def change_time_fomart(list_item):
    import time
    system_info = json.loads(file.read_file("./config/system.json"))
    if "time" in list_item and isinstance(list_item["time"], str):
        list_item["time"] = time.mktime(time.strptime(list_item["time"], system_info["Time_Format"]))
    return list_item


def main():
    if not os.path.exists("./backup"):
        os.mkdir("./backup")
    shutil.copytree("./config", "./backup/config")
    shutil.copytree("./document", "./backup/document")
    if os.path.exists("./templates/static/user_file"):
        shutil.copytree("./templates/static/user_file", "./backup/static/user_file")
    write_json = json.loads(file.read_file("./config/page.json"))
    write_json = list(map(change_time_fomart, write_json))
    file.write_file("./config/page.json", file.json_format_dump(write_json))

    for filename in os.listdir("./document/"):
        if filename.endswith(".json"):
            write_json = json.loads(file.read_file("./document/" + filename))
            write_json = change_time_fomart(write_json)
            file.write_file("./document/" + filename, json_format_dump(write_json))