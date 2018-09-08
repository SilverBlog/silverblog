#!/usr/bin/env bash

if [ -f "initialization.sh" ]; then
    cd ..
fi


if [ ! -f "./nginx_config" ]; then
echo "Generating Nginx configuration..."
cat << EOF >nginx_config
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:$(pwd)/config/unix_socks/main.sock;
    }
    location /control {
        include uwsgi_params;
        uwsgi_pass unix:$(pwd)/config/unix_socks/control.sock;
        add_header 'Access-Control-Allow-Origin' "https://c.silverblog.org";
	    add_header 'Access-Control-Allow-Credentials' "true";
	    add_header 'Access-Control-Allow-Origin' "https://c.silverblog.org";
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE';
        add_header 'Access-Control-Allow-Headers' 'reqid, nid, host, x-real-ip, x-forwarded-ip, event-type, event-id, accept, content-type';
        if (\$request_method = "OPTIONS") {
            return 204;
        }
    }
    location /static {
        alias $(pwd)/templates/static;
    }
}
EOF
fi


echo "Setup directories..."

mkdir ./document
mkdir -p ./config/unix_socks
mkdir -p ./templates/static
mkdir ./templates/include

touch ./templates/include/comment.html
touch ./templates/include/head.html
touch ./templates/include/foot.html

echo "Setup missing configuration files..."

if [ ! -f "./config/menu.json" ]; then
    echo "[]" > ./config/menu.json
fi

if [ ! -f "./config/page.json" ]; then
    echo "[]" > ./config/page.json
fi

if [ ! -f "./uwsgi.json" ]; then
    cp -i ./example/uwsgi.json ./uwsgi.json
fi

echo "Installation complete! "
echo -e "Note: \e[31;1;4mDO NOT\e[0m use \`git clean\` to reset your git repository. This command could potentially cause data loss!"