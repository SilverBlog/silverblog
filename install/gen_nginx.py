#!/usr/bin/env python3
import argparse
import os

nginx_template = \
    """
    map $http_origin $cors_origin {
        https://c.silverblog.org $http_origin;
        https://silvercreator.reallct.com $http_origin;
        default null;
    }
    server {
        ${listen_port}
        ${ssl_config}
        location / {
            include uwsgi_params;
            uwsgi_pass ${uwsgi_pass_main};
        }
        location /control {
            include uwsgi_params;
            uwsgi_pass ${uwsgi_pass_control};
            add_header 'Access-Control-Allow-Origin' $cors_origin;
            add_header 'Access-Control-Allow-Credentials' "true";
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE';
            add_header 'Access-Control-Allow-Headers' 'reqid, nid, host, x-real-ip, x-forwarded-ip, event-type, event-id, accept, content-type';
            if ($request_method = "OPTIONS") {
                return 204;
            }
        }
        location /static {
            alias ${pwd}/templates/static;
        }
    }
    """

if __name__ == '__main__':
    print("Generating Nginx configuration...")
    parser = argparse.ArgumentParser("Silverblog nginx profile creation tool")
    parser.add_argument("-t", "--tcp", help="", action="store_true")
    parser.add_argument("--host", help="", type=str, default="127.0.0.1")
    parser.add_argument("--main-port", help="", type=str, default="5000")
    parser.add_argument("--control-port", help="", type=str, default="5001")
    parser.add_argument("--ssl")

    args = parser.parse_args()
    pwd = os.getcwd()
    path_list = os.path.split(os.getcwd())
    if path_list[len(path_list) - 1] == "install":
        os.chdir(os.pardir)
        pwd = os.getcwd()
        print("Change directory to {}".format(pwd))
    if os.path.exists("nginx_config"):
        exit(0)
    uwsgi_pass_main = "unix:{pwd}/config/unix_socks/main.sock".format(pwd=pwd)
    uwsgi_pass_control = "unix:{pwd}/config/unix_socks/control.sock".format(pwd=pwd)
    if args.tcp:
        uwsgi_pass_main = "{}:{}".format(args.host, args.main - port)
        uwsgi_pass_control = "{}:{}".format(args.host, args.control - port)
    listen_port = "listen 80;"

    ssl_config = ""
    nginx_template = nginx_template.replace("${listen_port}", listen_port)
    nginx_template = nginx_template.replace("${ssl_config}", ssl_config)
    nginx_template = nginx_template.replace("${uwsgi_pass_main}", uwsgi_pass_main)
    nginx_template = nginx_template.replace("${uwsgi_pass_control}", uwsgi_pass_control)
    nginx_template = nginx_template.replace("${pwd}", pwd)
    with open("./nginx_config", "w", newline=None, encoding="utf-8") as f:
        f.write(nginx_template)
