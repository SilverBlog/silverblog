#!/usr/bin/env bash
command -v docker >/dev/null 2>&1 || { echo >&2 "This installation method relies on Docker, but does not find Docker. Please install Docker and try again."; exit 1; }

result=$(groups | grep "docker")
if [[ "$result" == "" ]]
then
    echo "The current user is not in the docker group,Adding user to docker user group."
    sudo gpasswd -a ${USER} docker

fi
docker pull silverblog/silverblog

#sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

cat << EOF > docker-compose.yml
version: '1'
services:
  silverblog:
    image: "silverBlog/silverblog"
    volumes:
     - ./template:/home/silverblog/templates
     - ./config:/home/silverblog/config
     - ./document:/home/silverblog/documents
    links:
     - silverblog_nginx
  silverblog_control:
    image: "silverBlog/silverblog"
    volumes:
     - ./template:/home/silverblog/templates
     - ./config:/home/silverblog/config
     - ./document:/home/silverblog/documents
    links:
     - silverblog_nginx
EOF

cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it -v ./:/home/silverblog -p 127.0.0.1:5000:5000 --restart="always" --name="silverblog"  silverblog/silverblog python3 manage.py
EOF
