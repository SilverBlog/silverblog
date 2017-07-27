#!/usr/bin/env bash
#NextMoe-icecat by 20170727 21:58
sudo pacman -S nginx uwsgi uwsgi-plugin-python python-pip python-wheel sudo gcc 

sudo pip install cffi
sudo pip install flask misaka 
sudo pip install pypinyin 
sudo pip install pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi
sudo chmod +x install.sh
./install.sh
 
