#!/usr/bin/env bash

git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 ./

if [ ! -f "./docker-compose.yml" ]; then
    cp -i ./example/docker-compose.example.yml ./docker-compose.yml
fi

cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it -v ./:/home/silverblog --name="silverblog_manage"  silverblog/silverblog python3 manage.py
EOF

./install/install.sh
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json




