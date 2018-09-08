#!/usr/bin/env bash
china_install=false
while getopts "n:c" arg; do
    case ${arg} in
         c)
            china_install=true
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./nginx_gen.sh [-c]"
            exit 1
            ;;
    esac
done

if [ -f "nginx_gen.sh" ]; then
    cd ..
fi


if [ ! -f "./nginx_config" ]; then
echo "Generating Nginx configuration..."
if [ ${china_install} = false ];then
gen_default_nginx
fi

if [ ${china_install} = true ];then
gen_china_nginx
fi
fi

function gen_default_nginx(){
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
}

function gen_china_nginx(){
cat << EOF >nginx_config
map \$http_origin \$cors_origin {
        https://c.silverblog.org \$http_origin;
        https://silvercreator.reallct.com \$http_origin;
        default null;
    }
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass unix:$(pwd)/config/unix_socks/main.sock;
    }
    location /control {
        include uwsgi_params;
        uwsgi_pass unix:$(pwd)/config/unix_socks/control.sock;
        add_header 'Access-Control-Allow-Origin' \$cors_origin;
	    add_header 'Access-Control-Allow-Credentials' "true";
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
}