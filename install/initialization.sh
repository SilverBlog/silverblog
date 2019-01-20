#!/usr/bin/env bash

if [[ -f "install.sh" ]]; then
    cd ..
    echo "Change directory to $(pwd)"
fi

echo "Setup directories..."

mkdir ./document
mkdir -p ./config/unix_socks
mkdir -p ./templates/static
mkdir ./templates/include

echo "Setup missing configuration files..."

if [[ ! -f "./config/menu.json" ]]; then
    echo "[]" > ./config/menu.json
fi

if [[ ! -f "./config/page.json" ]]; then
    echo "[]" > ./config/page.json
fi


echo "Installation complete! "
echo -e "Note: \e[31;1;4mDO NOT\e[0m use \`git clean\` to reset your git repository. This command could potentially cause data loss!"