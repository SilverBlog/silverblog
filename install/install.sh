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
            echo "use systemd_install.sh -n <project name> [-c]"
            echo "[-c] option represents using a Chinese image source."
            exit 1
            ;;
    esac
done

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

if command -v dnf >/dev/null 2>&1; then
    ${use_superuser} dnf -y update
    ${use_superuser} dnf -y install nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git curl gcc redhat-rpm-config python3-devel
    echo "{\"install\":\"dnf\"}" > install.lock
fi

if [ ! -f "install.lock" ]; then
    echo "The current system does not support local deployment. Please use Docker deployment."
    exit 1
fi

if [ ! -f "initialization.sh" ]; then
    if [ ! -d ${install_name} ]; then
        echo "Cloning silverblog..."

        repo_url=https://github.com/SilverBlogTeam/SilverBlog.git

        if [ -n ${china_install} ];then
            repo_url=https://gitee.com/qwe7002/silverblog.git
        fi

        git clone ${repo_url} --depth=1 ${install_name}
    fi
    mv install.lock ${install_name}/install/install.lock

    cd ${install_name}
    git fetch
    cd install
fi
./check_python_version.py

./install_python_dependency.sh

./initialization.sh

cd ..
cat << EOF >pm2.json
{
  "apps": [
    {
      "name": "${install_name}",
      "script": "/usr/bin/python3",
      "args": "watch.py",
      "merge_logs": true,
      "cwd": "./"
    },
    {
      "name": "${install_name}-control",
      "script": "/usr/bin/python3",
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

echo ""
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "./manage.py setting"
echo ""
echo "You can add the following code to .bashrc to quickly launch SilverBlog:"
echo ""
echo "${install_name}() {(cd \"$(pwd)\"&&./manage.py \$@)}"

