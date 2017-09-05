#!/usr/bin/env bash

echo "Installing Dependency..."

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog
fi

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
        include uwsgi_params;        uwsgi_pass 127.0.0.1:5001;
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
cp -i ./example/uwsgi.example.json ./uwsgi.json
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

cat << EOF >./start.sh
#!/usr/bin/env bash
docker run -t -i -v $x:/home/SilverBlog -p 5000:5000 silverblog uwsgi --json /home/SilverBlog/uwsgi.json --chdir /home/SilverBlog
EOF
cat << EOF >./control-start.sh
#!/usr/bin/env bash
docker run -t -i -v $x:/home/SilverBlog -p 5001:5001 silverblog uwsgi --json /home/SilverBlog/uwsgi.json:control --chdir /home/SilverBlog
EOF


chmod +x manage.py

echo "The installation is complete! Please edit $x/config/system.json file."