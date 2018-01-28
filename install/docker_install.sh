#!/usr/bin/env bash
command -v docker >/dev/null 2>&1 || { echo >&2 "This installation method relies on Docker, but does not find Docker. Please install Docker and try again."; exit 1; }

result=$(groups | grep "docker")
use_superuser=""
if [[ "$result" == "" ]]
then
    echo "The current user is not in the docker group,Adding user to docker user group."
    sudo gpasswd -a ${USER} docker

fi
docker pull silverblog/silverblog

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi

./install.sh

cd ..

sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

cat << EOF > docker-compose.yml
version: '1'
services:
  silverblog:
    image: "silverBlog/silverblog"
    ports:
     - "5000:5000"
    volumes:
     - ./:/home/silverblog
  silverblog_control:
    image: "silverBlog/silverblog"
    ports:
     - "5001:5001"
    volumes:
     - ./:/home/silverblog
EOF

cat << EOF >start.sh
#!/usr/bin/env bash
docker run -dt -v ./:/home/silverblog -p 127.0.0.1:5000:5000 --restart="always" --name="silverblog"  silverblog/silverblog
docker run -dt -v ./:/home/silverblog -p 127.0.0.1:5001:5001 --restart="always" --name="silverblog_control" silverblog/silverblog uwsgi --json uwsgi.json:control
EOF