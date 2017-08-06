#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Aisa/Shanghai)
sudo pacman -S nginx uwsgi uwsgi-plugin-python python-pip python-wheel sudo git gcc vim

sudo pip install cffi
sudo pip install flask 
sudo pip install misaka 
sudo pip install pypinyin 
sudo pip install pyrss2gen 
sudo pip install gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi
sudo chmod +x install.sh
./install.sh
 
