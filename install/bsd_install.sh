#!/usr/bin/env bash

set -o errexit

# shellcheck disable=SC2046
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi


install_name="silverblog"

while getopts "n" arg; do
    case ${arg} in
         n)
            install_name=$OPTARG
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./install.sh [-n <project name>] [-c]"
            exit 1
            ;;
    esac
done

function build_uwsgi_install(){
    if [[ ! -f "/usr/local/bin/uwsgi" ]]; then
        ${use_superuser} portsnap fetch extract update
        set +o errexit
        cd /usr/ports/devel/jansson/
        echo "Change directory to $(pwd)"
        ${use_superuser} make install clean
        cd -
        echo "Change directory to $(pwd)"
        set -o errexit
        echo "Downloading latest uWSGI tarball..."
        curl -o uwsgi_latest_from_installer.tar.gz http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
        mkdir uwsgi_latest_from_installer
        tar zvxC uwsgi_latest_from_installer --strip-components=1 -f uwsgi_latest_from_installer.tar.gz
        rm uwsgi_latest_from_installer.tar.gz
        cd uwsgi_latest_from_installer
        echo "Change directory to $(pwd)"
        ${use_superuser} python3 uwsgiconfig.py --build
        ${use_superuser} mv uwsgi /usr/local/bin/uwsgi
        cd ..
        echo "Change directory to $(pwd)"
        rm -rf uwsgi_latest_from_installer
    fi

}

function build_pip_install(){
    curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
    ${use_superuser} python3 get-pip.py
    rm get-pip.py
}

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

if command -v pkg >/dev/null 2>&1; then
    echo "The current package manager is pkg"
    echo "> ${use_superuser} pkg install newt nginx git python3"
    ${use_superuser} pkg install newt nginx git python3
    build_uwsgi_install
    build_pip_install
    echo "{\"install\":\"pkg\"}" > install.lock
fi


if [[ ! -f "install.lock" ]]; then
    echo "The current system does not support local deployment. Please use Docker deployment."
    exit 1
fi
if [[ ! -f "initialization.sh" ]]; then
    if [[ ! -d ${install_name} ]]; then
        echo -e "\nCloning silverblog..."
        git clone https://github.com/silverblogteam/silverblog.git ${install_name}
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
echo -e "> echo \"${install_name}() {(cd \"$(pwd)\"&&./manage.py \\\$@)}\" >> ${shell_config_file}"
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.py \\\$@)}" >> ${shell_config_file}
echo -e "\nTo get started you need Silverblog's bin directory (${shell_config_file}) in your PATH\n
environment variable. Next time you log in this will be done automatically.\n\n
To configure your current shell run source ${shell_config_file}"
fi

echo -e "> Silverblog successfully installed."
echo -e "\nYou need to perform [./manage.py] to initialize your silverblog environment."
echo -e "\nYou can generate an nginx configuration file using [./install/gen_nginx.py]."