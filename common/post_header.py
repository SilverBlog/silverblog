def add_post_header(list_item):
    if "name" in list_item:
        list_item["name"] = "post/{0}".format(list_item["name"])
    return list_item
