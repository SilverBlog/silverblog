#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Installing Dependency..."
$use_superuser pacman -Sy nginx uwsgi python libnewt uwsgi-plugin-python python-pip python-wheel git
$use_superuser pip install -r python_dependency.txt

read -p "Is qrcode support component installed? (Y/N): " yn

if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
    $use_superuser pip install qrcode-terminal
fi

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1
    cd SilverBlog/install
fi

if [ ! -f "../start.json" ]; then
    cp -i ../example/start.example.json ../start.json

fi
./install.sh
 
../setting.py