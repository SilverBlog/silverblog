#!/usr/bin/env sh

set -o errexit

templates_name="your template name"

if [ $(basename `pwd`) != "templates" ];then
    echo "[Error] Please do this in the templates directory!"
    exit
fi

if [ ! -d ${templates_name} ]; then
    echo "Cloning ${templates_name}..."
    git clone https://github.com/SilverBlogTheme/${templates_name}.git
fi

if [ ! -L ./static/${templates_name} ]; then
    echo "Create static file soft link..."
    ln -sv ../${templates_name}/static ./static/${templates_name}
fi

if [ -f "config.example.json" ]; then
    echo "Create a configuration file..."
    cp ${templates_name}/config.example.json ${templates_name}/config.json
fi

