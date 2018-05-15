#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Installing Dependency..."

if command -v apt-get >/dev/null 2>&1; then
    echo "Updating software source..."
    ${use_superuser} apt-get update
    ${use_superuser} apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git curl
    echo "{\"install\":\"apt-get\"}" > install.lock
fi

if command -v pacman >/dev/null 2>&1; then
    ${use_superuser} pacman -Sy nginx uwsgi python libnewt uwsgi-plugin-python python-pip python-wheel git gcc curl
    echo "{\"install\":\"pacman\"}" > install.lock
fi

if command -v yum >/dev/null 2>&1; then
    ${use_superuser} yum -y -v install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git curl gcc
    echo "{\"install\":\"yum\"}" > install.lock
fi
if [ ! -f "install.lock" ]; then
    echo "The current system does not support local deployment. Please use Docker deployment."
    exit 1
fi

if [ ! -f "initialization.sh" ]; then
    if [ ! -d "silverblog" ]; then
        echo "Cloning silverblog..."
        git clone https://github.com/SilverBlogTeam/SilverBlog.git --depth=1 silverblog
    fi
    mv install.lock silverblog/install/install.lock
    cd silverblog/install
fi

./check_python_version.py

./install_python_dependency.sh

./initialization.sh
