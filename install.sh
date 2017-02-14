#!/usr/bin/env bash
sudo apt-get install nginx uwsgi uwsgi-plugin-python3 python3-pip memcached clang python python3-dev libffi libffi-dev
sudo pip3 install -r python_package_list
mkdir document
cp ./config/menu.example.json menu.json
cp ./config/page.example.json page.json
python3 ./auto_config.py
