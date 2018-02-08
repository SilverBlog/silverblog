#!/usr/bin/env bash
command -v docker >/dev/null 2>&1 || { echo >&2 "This installation method relies on Docker, but does not find Docker. Please install Docker and try again."; exit 1; }

echo "Create directory..."

mkdir ./document
mkdir ./config
mkdir -p ./templates/static
mkdir ./templates/include

touch ./templates/include/comment.html
touch ./templates/include/head.html
touch ./templates/include/foot.html

echo "Create configuration file..."

if [ ! -f "./config/menu.json" ]; then
    echo "[]" > ./config/menu.json
fi
if [ ! -f "./config/page.json" ]; then
    echo "[]" > ./config/page.json
fi
if [ ! -f "./config/system.json" ]; then
    wget -O ./config/system.json https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/example/system.example.json
fi

wget -O ./docker-compose.yml https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/example/docker-compose.example.yml

cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it -v ./:/home/silverblog --name="silverblog_manage"  silverblog/silverblog python3 manage.py
EOF
