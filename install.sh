#!/usr/bin/env bash
sudo apt-get install nginx memcached uwsgi uwsgi-plugin-python3 python3-pip
sudo pip3 install cffi
sudo pip3 install -r python_package_list
git submodule init
git submodule update
mkdir document
mkdir templates
mkdir templates/static
cp config/menu.example.json config/menu.json
cp config/page.example.json config/page.json
cp config/system.example.json config/system.json
cp start.example.json start.json
cp start.example.sh start.sh
cp uwsgi.example.json uwsgi.json
chmod +x manage.py
chmod +x start.sh
vim config/system.json
cd templates/
ln -s $(pwd)/i-material/static $(pwd)/static/i-material
