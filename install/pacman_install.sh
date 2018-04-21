#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Installing Dependency..."
${use_superuser} pacman -Sy nginx uwsgi python libnewt uwsgi-plugin-python python-pip python-wheel git gcc curl


if [ ! -f "initialization.sh" ]; then
    echo "Cloning silverblog..."
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi
echo "{\"install\":\"pacman\"}" > install.lock

./check_python_version.py

./install_python_dependency.sh

./initialization.sh