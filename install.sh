#!/usr/bin/env bash
sudo apt-get install nginx memcached uwsgi uwsgi-plugin-python3 python3-pip 
sudo pip3 install cffi
sudo pip3 install -r ./python_package_list
git submodule init
cd ./templates/i-material
ln -s $(pwd)/static ../static/i-material
chmod +x manage.py
chmod +x start.sh
mkdir document
cp ./config/menu.example.json ./config/menu.json
cp ./config/page.example.json ./config/page.json
cp ./config/system.example.json ./config/system.json
cp ./start.example.json ./start.json
cp ./start.example.sh ./start.sh
cp ./uwsgi.example.json ./uwsgi.json
vim ./config/system.json