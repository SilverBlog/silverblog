#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
echo "Installing Dependency..."
pacman -S nginx uwsgi uwsgi-plugin-python python-pip python-wheel sudo git gcc vim

pip install cffi
pip install flask misaka pypinyin pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi
chmod +x install.sh
./install.sh
 
