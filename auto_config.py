import json

from common import file

system_name = input("请输入博客名称: ")
system_description = input("请输入博客简介:")
system_url = input("请输入访问URL:")
system_config = json.loads(file.read_file("./config/system.example.json"))
system_config["Project_Name"] = system_name
system_config["Project_Description"] = system_description
system_config["Project_URL"] = system_url
file.write_file("./config/system.json", json.dumps(system_config, ensure_ascii=False))
print("基本配置已完毕，您可以修改/config/system.json实现更多配置。")
