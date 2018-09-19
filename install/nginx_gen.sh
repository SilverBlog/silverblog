#!/usr/bin/env bash

china_install=false
tcp_install=false
while getopts "c:t" arg; do
    case ${arg} in
         t)
            tcp_install=true
            ;;
         c)
            china_install=true
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./nginx_gen.sh [-c] [-t]"
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


cors_setting="https://c.silverblog.org"
if [ ${china_install} = true ];then
cat << EOF >nginx_config
map \$http_origin \$cors_origin {
        https://c.silverblog.org \$http_origin;
        https://silvercreator.reallct.com \$http_origin;
        default null;
    }
EOF
cors_setting="\$cors_origin"
fi

uwsgi_pass_main="unix:$(pwd)/config/unix_socks/main.sock"
uwsgi_pass_control="unix:$(pwd)/config/unix_socks/control.sock"
if [ ${tcp_install} = true ];then
uwsgi_pass_main="127.0.0.1:5000"
uwsgi_pass_control="127.0.0.1:5001"
fi

cat << EOF >>nginx_config
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass ${uwsgi_pass_main};
    }
    location /control {
        include uwsgi_params;
        uwsgi_pass ${uwsgi_pass_control};
        add_header 'Access-Control-Allow-Origin' ${cors_setting};
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
fi