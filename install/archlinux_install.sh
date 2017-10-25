#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    echo "e.g. \"sudo $0\""
    exit 1
fi

echo "Installing Dependency..."
pacman -S nginx uwsgi uwsgi-plugin-python python-pip python-wheel git
pip install flask hoedown pypinyin pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1
    cd SilverBlog/install
fi

if [ ! -f "../start.json" ]; then
    cp -i ../example/start.example.json ../start.json

fi
./install.sh
 
python ../setting.py