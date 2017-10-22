print("If the upgrade process fails, please re-upgrade")
import os
import shutil

from common import file

def change_time_fomart(list_item):
    import time
    system_info = json.loads(file.read_file("./config/system.json"))
    list_item["time"] = time.mktime(time.strptime(list_item["time"], system_info["Time_Format"]))
    return list_item

shutil.copyfile("./config/page.json", "./config/page.json.bak")
write_json = json.loads(file.read_file("./config/page.json"))
write_json = list(map(change_time_fomart, write_json))
file.write_file("./config/page.json", json.dumps(write_json, indent=4, sort_keys=False, ensure_ascii=False))

for filename in os.listdir("./document/"):
    if filename.endswith(".json"):
        write_json = json.loads(file.read_file(filename))
        write_json = change_time_fomart(write_json)
        file.write_file(filename, json.dumps(write_json, indent=4, sort_keys=False, ensure_ascii=False))
