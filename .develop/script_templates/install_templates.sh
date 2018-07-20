#!/usr/bin/env bash

set -o errexit

templates_name="your template name"

if [ $(basename `pwd`) != "templates" ];then
    echo "[Error] Please do this in the templates directory!"
    exit
fi

if [ ! -d ${templates_name} ]; then
    git clone https://github.com/SilverBlogTheme/${templates_name}.git --depth=1
fi

ln -sv ../${templates_name}/static ./static/${templates_name}

cd ${templates_name}

if [ -f "config.example.json" ]; then
    cp config.example.json config.json
fi