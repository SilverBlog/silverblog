#!/usr/bin/env bash
cd ..

cat << EOF >nginx_example
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000;
    }
    location /control {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5001;
    }
    location /static {
        alias $(pwd)/templates/static;
    }
}
EOF

sudo pip3 install cffi
sudo pip3 install flask misaka pypinyin pyrss2gen
git submodule init
git submodule update
mkdir document
mkdir templates
mkdir templates/static
cp config/menu.example.json config/menu.json
cp config/page.example.json config/page.json
cp config/system.example.json config/system.json
cp example/start.example.json start.json
cp example/start.example.sh start.sh
cp example/uwsgi.example.json uwsgi.json
chmod +x manage.py
vim config/system.json
cd templates/i-material
ln -s $(pwd)/static ../static/i-material
