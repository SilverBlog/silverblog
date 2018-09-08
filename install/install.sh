#!/usr/bin/env bash

set -o errexit

if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

china_install=false
install_name="silverblog"

while getopts "n:c" arg; do
    case ${arg} in
         n)
            install_name=$OPTARG
            ;;
         c)
            china_install=true
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./install.sh -n <project name> [-c]"
            echo "[-c] option represents using a Chinese image source."
            exit 1
            ;;
    esac
done

function build_uwsgi_install(){
    if [ ! -f "/usr/local/bin/uwsgi" ]; then
        ${use_superuser} portsnap fetch extract update
        set +o errexit
        cd /usr/ports/devel/jansson/
        ${use_superuser} make install clean
        cd -
        set -o errexit
        echo "Downloading latest uWSGI tarball..."
        curl -o uwsgi_latest_from_installer.tar.gz http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
        mkdir uwsgi_latest_from_installer
        tar zvxC uwsgi_latest_from_installer --strip-components=1 -f uwsgi_latest_from_installer.tar.gz
        rm uwsgi_latest_from_installer.tar.gz
        cd uwsgi_latest_from_installer
        ${use_superuser} python3 uwsgiconfig.py --build
        ${use_superuser} sudo mv uwsgi /usr/local/bin/uwsgi
        cd ..
        rm -rf uwsgi_latest_from_installer
    fi

}

function build_pip_install(){
    curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
    ${use_superuser} python3 get-pip.py
    rm get-pip.py
}

use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

echo "Installing Dependency..."

if command -v pkg >/dev/null 2>&1; then
    ${use_superuser} pkg install -y newt nginx git python3
    build_uwsgi_install
    build_pip_install
    echo "{\"install\":\"pkg\"}" > install.lock
fi

if command -v pkgin >/dev/null 2>&1; then
    ${use_superuser} pkgin install -y newt nginx git python3
    build_uwsgi_install
    build_pip_install
    echo "{\"install\":\"pkgin\"}" > install.lock
fi


if command -v apt-get >/dev/null 2>&1; then
    ${use_superuser} apt-get update
    ${use_superuser} apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git
    echo "{\"install\":\"apt-get\"}" > install.lock
fi

if command -v pacman >/dev/null 2>&1; then
    ${use_superuser} pacman -Sy nginx uwsgi python python-pip python-wheel libnewt uwsgi-plugin-python git gcc
    echo "{\"install\":\"pacman\"}" > install.lock
fi

if command -v dnf >/dev/null 2>&1; then
    ${use_superuser} dnf -y install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-devel python3-wheel git gcc redhat-rpm-config
    echo "{\"install\":\"dnf\"}" > install.lock
fi

if command -v apk >/dev/null 2>&1; then
    ${use_superuser} apk add --no-cache --update procps
    ${use_superuser} apk add --no-cache python3 python3-dev git uwsgi uwsgi-python3 newt ca-certificates musl-dev gcc python3-dev nginx
    echo "{\"install\":\"apk\"}" > install.lock
fi


if [ ! -f "install.lock" ]; then
    echo "The current system does not support local deployment. Please use Docker deployment."
    exit 1
fi

if [ ! -f "initialization.sh" ]; then
    if [ ! -d ${install_name} ]; then
        echo "Cloning silverblog..."

        repo_url=https://github.com/silverblogteam/silverblog.git

        if [ ${china_install} = true ];then
            repo_url=https://code.aliyun.com/silverblogteam/silverblog.git
        fi

        git clone ${repo_url} --depth=1 ${install_name}
    fi
    mv install.lock ${install_name}/install/install.lock

    cd ${install_name}
    git fetch
    cd install
fi

python3 ./check_python_version.py

bash ./install_python_dependency.sh

bash ./initialization.sh

if [ ${china_install} = true ]; then
china_option="-c"
fi

bash ./nginx_gen.sh ${china_option}
cd ..

read -p "Create a pm2 configuration file? (Y/N) :" yn

if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
cat << EOF >pm2.json
{
    "apps": [
        {
        "name": "${install_name}-main",
        "script": "python3",
        "args": "watch.py",
        "merge_logs": true,
        "cwd": "./"
        },
        {
        "name": "${install_name}-control",
        "script": "python3",
        "args": [
            "watch.py",
            "--control"
        ],
        "merge_logs": true,
        "cwd": "./"
        }
    ]
}
EOF
fi
if [ "$yn" == "N" ] || [ "$yn" == "n" ]; then
read -p "Create a supervisord configuration file? (Y/N) :" yn
if [ "$yn" == "Y" ] || [ "$yn" == "y" ]; then
cat << EOF >supervisord.conf
[program:${install_name}-main]
command=./watch.py
directory=$(pwd)
autorestart=true

[program:${install_name}-control]
directory=$(pwd)
command=./watch.py --control
autorestart=true
EOF
fi
fi
echo ""
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "./manage.py"
echo ""
echo "You can add the following code to .bashrc to quickly launch SilverBlog:"
echo ""
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.py \$@)}"

