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
        ${server_name}
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
    ${http_to_https}
    """

if __name__ == '__main__':
    print("Generating Nginx configuration...")
    parser = argparse.ArgumentParser("Silverblog nginx profile creation tool")
    parser.add_argument("--force", help="Force the generation of the nginx configuration file.", action="store_true")
    parser.add_argument("--domain", help="The domain name of the website.", type=str)
    parser.add_argument("--pwd", help="Current website directory.", type=str)
    parser.add_argument("--host", help="uwsgi listens for the address.", type=str)
    parser.add_argument("--main_port", help="The main service listening port.", type=str)
    parser.add_argument("--control_port", help="The Control service listening port.", type=str)
    parser.add_argument("--cert_key", help="SSL certificate key.", type=str)
    parser.add_argument("--cert_fullchain", help="SSL certificate fullchain.", type=str)
    parser.add_argument("--hsts", help="Use HSTS.", action="store_true")
    parser.add_argument("--ocsp_must_staple", help="Use OCSP Must-Staple.", action="store_true")

    args = parser.parse_args()
    pwd = None
    if args.pwd is not None:
        pwd = args.pwd
    if pwd is None:
        pwd = os.getcwd()
    path_list = os.path.split(os.getcwd())
    if path_list[len(path_list) - 1] == "install":
        os.chdir(os.pardir)
        pwd = os.getcwd()
        print("Change directory to {}".format(pwd))
    if not args.force and os.path.exists("nginx_config"):
        print("The file exists and skips the build.")
        exit(0)
    uwsgi_pass_main = "unix:{pwd}/config/unix_socks/main.sock".format(pwd=pwd)
    uwsgi_pass_control = "unix:{pwd}/config/unix_socks/control.sock".format(pwd=pwd)
    if args.host is not None and args.main_port is not None and args.control_port is not None:
        uwsgi_pass_main = "{}:{}".format(args.host, args.main_port)
        uwsgi_pass_control = "{}:{}".format(args.host, args.control_port)
    listen_port = "listen 80;"
    server_name = ""
    if args.domain is not None:
        server_name = "server_name {};".format(args.domain)
    ssl_config = ""
    http_to_https = ""
    if args.cert_key is not None and args.cert_fullchain is not None:
        listen_port = "listen 443 ssl http2;"
        hsts = ""
        ocsp = ""
        if args.hsts:
            hsts = "add_header Strict-Transport-Security \"max-age=31536000;\" always;"
        if args.ocsp_must_staple:
            ocsp = """ssl_stapling on;
            ssl_stapling_verify on;
            """
        ssl_config = """${hsts}
        ${ocsp}
        ssl_certificate ${ssl_fullchain};
        ssl_certificate_key ${ssl_key};
        ssl_prefer_server_ciphers on;
        ssl_protocols TLSv1.3 TLSv1.2 TLSv1.1;
        ssl_ciphers "TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-256-GCM-SHA256:TLS13-AES-256-CCM-8-SHA256:TLS13-AES-256-CCM-SHA256:EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+ECDSA+AES256:EECDH+aRSA+AES256:RSA+AES256:EECDH+ECDSA+AES256:EECDH+aRSA+AES256:RSA+AES256:EECDH+ECDSA+3DES:EECDH+aRSA+3DES:RSA+3DES:!MD5";
        keepalive_timeout 70;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        """
        ssl_config = ssl_config.replace("${ssl_fullchain}", args.cert_fullchain)
        ssl_config = ssl_config.replace("${ssl_key}", args.cert_key)
        ssl_config = ssl_config.replace("${hsts}", hsts)
        ssl_config = ssl_config.replace("${ocsp}", ocsp)
        http_to_https = """
        server {
            listen 80;
            ${server_name}
            location / {
	            return 301 https://${domain}$request_uri;
            }
        }
        """
        http_to_https = http_to_https.replace("${domain}", args.domain)
        http_to_https = http_to_https.replace("${server_name}", server_name)
    nginx_config = nginx_template.replace("${listen_port}", listen_port)
    nginx_config = nginx_config.replace("${server_name}", server_name)
    nginx_config = nginx_config.replace("${ssl_config}", ssl_config)
    nginx_config = nginx_config.replace("${http_to_https}", http_to_https)
    nginx_config = nginx_config.replace("${uwsgi_pass_main}", uwsgi_pass_main)
    nginx_config = nginx_config.replace("${uwsgi_pass_control}", uwsgi_pass_control)
    nginx_config = nginx_config.replace("${pwd}", pwd)
    with open("./nginx_config", "w", newline=None, encoding="utf-8") as f:
        print("Write the file: [./nginx_config]")
        f.write(nginx_config)
