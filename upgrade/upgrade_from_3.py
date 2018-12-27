import hashlib
import hmac
import json
import shutil
import uuid

from common import file


def add_page_id(list_item):
    list_item["uuid"] = str(uuid.uuid5(uuid.NAMESPACE_URL, list_item["name"]))
    return list_item


def add_menu_id(list_item):
    if "name" in list_item:
        return add_page_id(list_item)
    return list_item

def main():
    shutil.copyfile("./config/page.json", "./config/page.json.bak")
    shutil.copyfile("./config/menu.json", "./config/menu.json.bak")
    page_list = json.loads(file.read_file("./config/page.json"))
    page_list = list(map(add_page_id, page_list))
    menu_list = json.loads(file.read_file("./config/menu.json"))
    menu_list = list(map(add_menu_id, menu_list))

    file.write_file("./config/page.json", file.json_format_dump(page_list))
    file.write_file("./config/menu.json", file.json_format_dump(menu_list))

    system_config = json.loads(file.read_file("./config/system.json"))
    control_config = dict()
    try:
        old_password_hash = json.loads(system_config["API_Password"])["hash_password"]
    except (ValueError, KeyError, TypeError):
        return

    control_config["password"] = hmac.new(str("SiLvErBlOg").encode('utf-8'), str(old_password_hash).encode('utf-8'),
                                          hashlib.sha256).hexdigest()
    del system_config["API_Password"]
    shutil.copyfile("./config/system.json", "./config/system.json.bak")
    file.write_file("./config/system.json", file.json_format_dump(system_config))
    file.write_file("./config/control.json", file.json_format_dump(control_config))


if __name__ == '__main__':
    main()
