#!/usr/bin/env bash

use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

V1=3
V2=4
echo need python version is : $V1.$V2
U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
echo your python version is : $U_V1.$U_V2

if [ $U_V1 -lt $V1 ];then
    echo 'The current Python version is below 3.4 and can not install SilverBlog'
    exit 1
fi
if [ $U_V2 -lt $V2 ];then
    echo 'The current Python version is below 3.4 and can not install SilverBlog'
    exit 1
fi

echo "Updating software source..."

${use_superuser} apt-get update

echo "Installing Dependency..."

${use_superuser} apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git
${use_superuser} pip3 install -r python_dependency.txt

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    cd silverblog/install
fi

if [ ! -f "../start.json" ]; then
    cp -i ../example/pm2.example.json ../pm2.json
fi

read -p "Is qrcode support component installed? (Y/N): " yn

if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
    ${use_superuser} pip3 install qrcode-terminal
fi

./install.sh
python3 manage.py setting