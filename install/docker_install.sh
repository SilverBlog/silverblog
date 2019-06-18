#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi
if [[ $UID -eq 0 ]]; then
    read -p "Running this script as root can damage your system. Continue to execute? (y/N) :" yn
    if [[ "$yn" != "Y" ]] || [[ "$yn" != "y" ]]; then
        exit 0
    fi
fi

install_name="silverblog"

while getopts "n" arg; do
    case ${arg} in
         n)
            install_name=$OPTARG
            ;;
         ?)
            echo "Unknown argument"
            echo "use ./docker_install.sh [-n <project name>] [-c]"
            exit 1
            ;;
    esac
done

if [[ ! -f "initialization.sh" ]]; then
    if [[ ! -d ${install_name} ]]; then
        echo "Cloning silverblog..."
        git clone https://github.com/SilverBlogTeam/SilverBlog.git ${install_name}
    fi
    cd ${install_name}
    echo "Change directory to $(pwd)"
    git fetch
    cd install
    echo "Change directory to $(pwd)"
fi

echo "{\"install\":\"docker\"}" > install.lock

cd ..
echo "Change directory to $(pwd)"

bash install/initialization.sh

if [[ ! -f "./supervisor.conf" ]]; then
cp ./example/supervisor.conf ./supervisor.conf
fi

if [[ ! -f "./docker-compose.yml" ]]; then
cat << EOF > docker-compose.yml
version: '3'
services:
  ${install_name}:
    image: silverblog/silverblog
    container_name: "${install_name}"
    restart: on-failure:10
    command: /usr/bin/supervisord -c /home/silverblog/supervisor.conf
    volumes:
     - /etc/localtime:/etc/localtime:ro
     - $(pwd):/home/silverblog/
EOF
fi


if test $(ps h -o comm -p $$) = "bash"; then
shell_config_file="$HOME/.bashrc"
if [[ -f "$HOME/.bash_profile" ]]; then
shell_config_file="~/.bash_profile"
fi
fi

if test $(ps h -o comm -p $$) = "zsh"; then
if [[ -f "$HOME/.zshrc" ]]; then
shell_config_file="$HOME/.zshrc"
fi
fi

read -p  "add command [${install_name}] to quickly launch SilverBlog? (y/N)" yn
if [[ "$yn" == "Y" ]] || [[ "$yn" == "y" ]]; then
echo -e "\n> echo \"${install_name}() {(cd \"$(pwd)\"&&./manage.py \\\$@)}\" >> ${shell_config_file}"
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.py \\\$@)}" >> ${shell_config_file}
fi

echo -e "\n> Silverblog successfully installed."
echo -e "\nYou need to perform [./manage.py] to initialize your silverblog environment."
echo -e "\nIMPORTANT: OPEN A NEW TERMINAL TAB/WINDOW or run `. ${shell_config_file}`before using Silverblog."
echo -e "\nYou can generate an nginx configuration file using [./install/gen_nginx.py]."