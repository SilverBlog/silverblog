#!/usr/bin/env bash

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1
    cd SilverBlog/install
fi

./install.sh

cd ..

sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json