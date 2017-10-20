#!/usr/bin/env bash
docker pull qwe7002/silverblog

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1
    cd SilverBlog/install
fi

./install.sh

cd ..

sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

cat << EOF >start.sh
#!/usr/bin/env bash
docker run -dit -v $(pwd):/home/SilverBlog -p 5000:5000 qwe7002/silverblog python3 watch.py --docker
docker run -dit -v $(pwd):/home/SilverBlog -p 5001:5001 qwe7002/silverblog uwsgi --json uwsgi.json:control
EOF
cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it -v $(pwd):/home/SilverBlog qwe7002/silverblog python3 manage.py \$*
EOF

chmod +x manage.sh