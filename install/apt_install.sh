#!/usr/bin/env bash

use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Updating software source..."

${use_superuser} apt-get update

echo "Installing Dependency..."

${use_superuser} apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git curl

if [ ! -f "initialization.sh" ]; then
    echo "Cloning silverblog..."
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi

echo "{\"install\":\"apt-get\"}" > install.lock

./check_python_version.py

./install_python_dependency.sh

read -p "Is qrcode support component installed? (Y/N): " yn

if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
    ${use_superuser} python3 -m pip install qrcode-terminal
fi

./initialization.sh
