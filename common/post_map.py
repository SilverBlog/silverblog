import time

def add_post_header(list_item):
    if "name" in list_item:
        list_item["name"] = "post/{0}".format(list_item["name"])
    return list_item

def build_time(time_s, system_info):
    return time.strftime(system_info["Time_Format"], time.localtime(time_s))
