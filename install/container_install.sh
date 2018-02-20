#!/usr/bin/env bash
if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi
./install.sh
cd ..
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "python3 manage.py setting"