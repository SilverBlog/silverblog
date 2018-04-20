# -*- coding: utf-8 -*-
print("If the upgrade process fails, please re-upgrade")
import json
import os
import shutil

def read_file(filename):
    f = open(filename, newline=None)
    content = f.read()
    return content

def write_file(filename, content):
    f = open(filename, "w", newline=None)
    f.write(content)
    f.close()

def change_time_fomart(list_item):
    import time
    system_info = json.loads(read_file("./config/system.json"))
    if "time" in list_item and isinstance(list_item["time"], str):
        list_item["time"] = time.mktime(time.strptime(list_item["time"], system_info["Time_Format"]))
    return list_item

shutil.copyfile("./config/page.json", "./config/page.json.bak")
write_json = json.loads(read_file("./config/page.json"))
write_json = list(map(change_time_fomart, write_json))
write_file("./config/page.json", json.dumps(write_json, indent=4, sort_keys=False, ensure_ascii=False))

for filename in os.listdir("./document/"):
    if filename.endswith(".json"):
        write_json = json.loads(read_file("./document/" + filename))
        write_json = change_time_fomart(write_json)
        write_file("./document/" + filename, json.dumps(write_json, indent=4, sort_keys=False, ensure_ascii=False))
