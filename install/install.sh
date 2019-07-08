#!/usr/bin/env bash

set -o errexit

if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi


install_name="silverblog"
install_branch="master"
while getopts "n:c:" arg; do
    case ${arg} in
         n)
            install_name=$OPTARG
            ;;
         c)
            install_branch=$OPTARG
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./install.sh [-n <project name>] [-c <Install channel name>]"
            exit 1
            ;;
    esac
done


use_superuser=""
if [[ $UID -ne 0 ]]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

if [[ -f "README.md" ]]; then
    if [[ -d "install" ]]; then
        cd install
        echo "Change directory to $(pwd)"
    fi
fi

echo -e "\nInstalling Dependency..."

if command -v apt-get >/dev/null 2>&1; then
    echo "The current package manager is apt-get"
    echo "> ${use_superuser} apt-get update"
    ${use_superuser} apt-get update
    echo "> ${use_superuser} apt-get install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git"
    ${use_superuser} apt-get install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git
    echo "{\"install\":\"apt-get\"}" > install.lock
fi

if command -v pacman >/dev/null 2>&1; then
    echo "The current package manager is pacman"
    echo "> ${use_superuser} pacman -S nginx uwsgi python python-pip python-wheel libnewt uwsgi-plugin-python git gcc"
    ${use_superuser} pacman -S nginx uwsgi python python-pip python-wheel libnewt uwsgi-plugin-python git gcc
    echo "{\"install\":\"pacman\"}" > install.lock
fi

if command -v dnf >/dev/null 2>&1; then
    echo "The current package manager is dnf"
    echo "> ${use_superuser} dnf install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-devel python3-wheel git gcc redhat-rpm-config"
    ${use_superuser} dnf install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-devel python3-wheel git gcc redhat-rpm-config
    echo "{\"install\":\"dnf\"}" > install.lock
fi

if command -v apk >/dev/null 2>&1; then
    echo "The current package manager is apk"
    echo "> ${use_superuser} apk add --no-cache --update procps"
    ${use_superuser} apk add --no-cache --update procps
    echo "> ${use_superuser} apk add --no-cache python3 python3-dev git uwsgi uwsgi-python3 newt ca-certificates musl-dev gcc python3-dev nginx"
    ${use_superuser} apk add --no-cache python3 python3-dev git uwsgi uwsgi-python3 newt ca-certificates musl-dev gcc python3-dev nginx
    echo "{\"install\":\"apk\"}" > install.lock
fi


if [[ ! -f "install.lock" ]]; then
    echo "The current system does not support local deployment. Please use Docker deployment."
    exit 1
fi
if [[ ! -f "initialization.sh" ]]; then
    if [[ ! -d ${install_name} ]]; then
        echo -e "\nCloning silverblog..."
        git clone -b ${install_branch} https://github.com/silverblog/silverblog.git ${install_name}
    fi
    mv install.lock ${install_name}/install/install.lock

    cd ${install_name}
    echo "Change directory to $(pwd)"
    git fetch
    cd install
    echo "Change directory to $(pwd)"

fi

echo -e "> ./install_denpendency.py"
python3 ./install_denpendency.py
echo -e "> ./initialization.sh"
bash ./initialization.sh
read -p "Use systemd to manage startup? (y/N) :" yn
if [[ "$yn" == "Y" ]] || [[ "$yn" == "y" ]]; then
bash ./systemd_install.sh -n ${install_name}
fi
cd ..
echo "Change directory to $(pwd)"
if [[ "$yn" != "Y" ]] && [[ "$yn" != "y" ]]; then
read -p "Create a pm2 configuration file? (y/N) :" yn
if [[ "$yn" == "Y" ]] || [[ "$yn" == "y" ]]; then
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
fi
if [[ "$yn" != "Y" ]] && [[ "$yn" != "y" ]]; then
read -p "Create a supervisord configuration file? (y/N) :" yn
if [[ "$yn" == "Y" ]] || [[ "$yn" == "y" ]]; then
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

# shellcheck disable=SC2046
if test $(ps h -o comm -p $$) = "bash"; then
shell_config_file="$HOME/.bashrc"
if [[ -f "$HOME/.bash_profile" ]]; then
shell_config_file="/.bash_profile"
fi
fi

# shellcheck disable=SC2046
if test $(ps h -o comm -p $$) = "zsh"; then
if [[ -f "$HOME/.zshrc" ]]; then
shell_config_file="$HOME/.zshrc"
fi
fi

read -p  "add command [${install_name}] to quickly launch SilverBlog? (y/N)" yn
if [[ "$yn" == "Y" ]] || [[ "$yn" == "y" ]]; then
echo -e "> echo \"${install_name}() {(cd \"$(pwd)\"&&./manage.py \$@)}\" >> ${shell_config_file}"
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.py \\\$@)}" >> ${shell_config_file}
echo -e "\nTo get started you need Silverblog's bin directory (${shell_config_file}) in your PATH\n
environment variable. Next time you log in this will be done automatically.\n\n
To configure your current shell run source ${shell_config_file}"
fi

echo -e "> Silverblog successfully installed."
echo -e "\nYou need to perform [./manage.py] to initialize your silverblog environment."
echo -e "\nYou can generate an nginx configuration file using [./install/gen_nginx.py]."