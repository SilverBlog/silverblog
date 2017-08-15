#!/usr/bin/env bash

echo "Updating software source..."

apt-get update

echo "Installing Dependency..."

apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git
pip3 install cffi
pip3 install flask misaka pypinyin pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi
sudo chmod +x install.sh
./install.sh