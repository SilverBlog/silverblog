#!/usr/bin/env bash

if [ ! -f "initialization.sh" ]; then
    echo "Cloning silverblog..."
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi

echo "{\"install\":\"docker\"}" > install.lock
./initialization.sh
cd ..
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json
if [ ! -f "./docker-compose.yml" ]; then
    cp -i ./example/docker-compose.yml ./docker-compose.yml
fi
cat << EOF >manage.sh
#!/usr/bin/env bash
docker exec -it silverblog python3 manage.py \$@
EOF
chmod +x manage.sh
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "docker run -i -v \$(pwd):/home/silverblog --name=\"silverblog_manage\" silverblog/silverblog python3 manage.py setting"