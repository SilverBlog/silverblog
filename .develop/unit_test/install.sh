#!/usr/bin/env bash
sed -i '''s/deb-src/#deb-src/g' /etc/apt/sources.list
apt-get update
apt-get -y install python3-socks nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git curl python3-flask python3-pyrss2gen python3-requests python3-watchdog
python3 -m pip install hoedown xpinyin gitpython
cd install
echo "{\"install\":\"apt-get\"}" > install.lock
bash initialization.sh
cd ..
cp -f ./.develop/demo/page.json ./config/page.json
cp -f ./.develop/demo/menu.json ./config/menu.json
cp -f ./.develop/demo/system.json ./config/system.json
cp ./.develop/demo/demo-article.md ./document/demo-article.md
python3 manage.py update
cd ./templates
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"
cd ..
rm /etc/nginx/sites-enabled/default
echo "Generating Nginx configuration..."

if [ ! -f "./nginx_config" ]; then
cat << EOF >/etc/nginx/sites-enabled/default
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

echo "{\"excerpt\":\"this is a test\",\"time\":0}" > ./document/demo-article.json
