#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Installing Dependency..."
${use_superuser} pacman -Sy nginx uwsgi python libnewt uwsgi-plugin-python python-pip python-wheel git


if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi

./install_python_dependency.sh

if [ ! -f "../pm2.json" ]; then
    cp -i ../example/pm2.json ../pm2.json
fi

read -p "Is qrcode support component installed? (Y/N): " yn

if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
    ${use_superuser} pip install qrcode-terminal
fi

./install.sh