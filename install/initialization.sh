#!/usr/bin/env bash
if [ -f "initialization.sh" ]; then
    cd ..
fi
echo "Generating Nginx configuration..."

if [ ! -f "./nginx_config" ]; then
cat << EOF >nginx_config
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000;
    }
    location /control {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5001;
        add_header 'Access-Control-Allow-Origin' "https://c.silverblog.org";
	    add_header 'Access-Control-Allow-Credentials' "true";
        if (\$request_method = "OPTIONS") {
            add_header 'Access-Control-Allow-Origin' "https://c.silverblog.org";
            add_header 'Access-Control-Max-Age' 86400;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE';
            add_header 'Access-Control-Allow-Headers' 'reqid, nid, host, x-real-ip, x-forwarded-ip, event-type, event-id, accept, content-type';
            add_header 'Content-Length' 0;
            add_header 'Content-Type' 'text/plain, charset=utf-8';
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
mkdir ./config
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
if [ ! -f "./config/system.json" ]; then
    cp -i ./example/system.json ./config/system.json
fi
if [ ! -f "./uwsgi.json" ]; then
    cp -i ./example/uwsgi.json ./uwsgi.json
fi

echo "Installation complete! "
echo -e "Note: \e[31;1;4mDO NOT\e[0m use \`git clean\` to reset your git repository. This command could potentially cause data loss!"