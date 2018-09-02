#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

china_install=false
install_name="silverblog"

while getopts "n:c" arg; do
    case ${arg} in
         n)
            install_name=$OPTARG
            ;;
         c)
            china_install=true
            ;;
         ?)
            echo "Unknown argument"
            exit 1
            ;;
    esac
done

docker_image="silverblog/silverblog"
repo_url=https://github.com/SilverBlogTeam/SilverBlog.git

if [ -n ${china_install} ];then
    docker_image="registry.cn-hangzhou.aliyuncs.com/silverblog/silverblog"
    repo_url=https://gitee.com/qwe7002/silverblog.git
fi

if [ ! -f "initialization.sh" ]; then
    if [ ! -d ${install_name} ]; then
        echo "Cloning silverblog..."
        git clone ${repo_url} --depth=1 ${install_name}
    fi
    cd ${install_name}
    git fetch
    cd install
fi

echo "{\"install\":\"docker\"}" > install.lock

cd ..

if [ ! -f "../nginx_config" ]; then
echo "Generating Nginx configuration..."
cat << EOF >../nginx_config
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
bash install/initialization.sh
sed -i '''s/.\/config\/unix_socks\/main.sock/0.0.0.0:5000/g' uwsgi.json
sed -i '''s/.\/config\/unix_socks\/control.sock/0.0.0.0:5001/g' uwsgi.json
if [ ! -f "./docker-compose.yml" ]; then
cat << EOF > docker-compose.yml
version: '3'
services:
  ${install_name}:
    image: "${docker_image}"
    container_name: "${install_name}"
    restart: on-failure:10
    command: python3 watch.py
    volumes:
     - $(pwd):/home/silverblog/
    ports:
     - "127.0.0.1:5000:5000"
  ${install_name}_control:
    image: "${docker_image}"
    container_name: "${install_name}_control"
    restart: on-failure:10
    command: python3 watch.py --control
    volumes:
     - $(pwd):/home/silverblog/
    ports:
     - "127.0.0.1:5001:5001"
EOF
fi

if [ ! -f "./docker-compose-with-nginx.yml" ]; then
cat << EOF > docker-compose-with-nginx.yml
version: '3'
services:
  ${install_name}:
    image: "${docker_image}"
    container_name: "${install_name}"
    restart: on-failure:10
    command: python3 watch.py
    networks:
      ${install_name}_net:
        ipv4_address: 172.18.0.1
    volumes:
     - $(pwd):/home/silverblog/
  ${install_name}_control:
    image: "${docker_image}"
    container_name: "${install_name}_control"
    restart: on-failure:10
    command: python3 watch.py --control
    networks:
      ${install_name}_net:
        ipv4_address: 172.18.0.2
    volumes:
     - $(pwd):/home/silverblog/
  ${install_name}_nginx:
    image:"nginx:alpine"
    container_name: "${install_name}_nginx"
    restart: on-failure:10
    command: cp $(pwd)/nginx_config /etc/nginx/conf.d/default.conf && sed -i '''s/127.0.0.1:5000/172.18.0.1/g' && sed -i '''s/127.0.0.1:5001/172.18.0.2/g' && nginx -g daemon off;
    networks:
      ${install_name}_net:
        ipv4_address: 172.18.0.3
    ports:
      - 80:80
    volumes:
      - $(pwd):$(pwd)
networks:
  ${install_name}_net:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.16.0.0/24
EOF
fi

cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it --rm -v \$(pwd):/home/silverblog --name="${install_name}_manage" silverblog/silverblog python3 manage.py \$@
EOF
chmod +x manage.sh

echo ""
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "./manage.sh"
echo ""
echo "You can add the following code to .bashrc to quickly launch SilverBlog."
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.sh \$@)}"
