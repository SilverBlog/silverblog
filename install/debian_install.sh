#!/usr/bin/env bash

if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    echo "e.g. \"sudo $0\""
    exit 1
fi

echo "Updating software source..."

apt-get update

echo "Installing Dependency..."

apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git
pip3 install flask hoedown pypinyin pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1
    cd SilverBlog/install
fi

if [ ! -f "../start.json" ]; then
    cp -i ../example/start.json ../start.json

fi

./install.sh
../setting.py