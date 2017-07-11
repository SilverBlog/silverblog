#!/usr/bin/env bash
sudo apt-get install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel
sudo pip3 install cffi
sudo pip3 install flask misaka pypinyin pyrss2gen qrcode-terminal
./install.sh