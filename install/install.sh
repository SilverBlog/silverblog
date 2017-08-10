#!/usr/bin/env bash
cd ..

echo "Generate a Nginx configuration file..."

x=$(pwd)

cat << EOF >nginx_config
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000;
    }
    location /control {
        add_header 'Access-Control-Allow-Origin' 'https://silverblog.org';
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5001;
    }
    location /static {
        alias $x/templates/static;
    }
}
EOF

echo "Create directory..."

mkdir ./document
mkdir ./templates
mkdir ./templates/static
mkdir ./config

echo "Create configuration file..."

cp -i ./example/menu.example.json ./config/menu.json
cp -i ./example/page.example.json ./config/page.json
cp -i ./example/system.example.json ./config/system.json

cp -i ./example/start.example.json ./start.json
cp -i ./example/start.example.sh ./start.sh
cp -i ./example/control-start.example.sh ./control-start.sh
cp -i ./example/uwsgi.example.json ./uwsgi.json

chmod +x manage.py

echo "The installation is complete! Please edit $x/config/system.json file."