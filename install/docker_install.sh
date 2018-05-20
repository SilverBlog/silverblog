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
            exit 1
            ;;
    esac
done

if [ ! -f "initialization.sh" ]; then
    if [ ! -d ${install_name} ]; then
        echo "Cloning silverblog..."

        repo_url=https://github.com/SilverBlogTeam/SilverBlog.git
        if [ -n ${china_install} ];then
            repo_url=https://gitee.com/qwe7002/silverblog.git
        fi

        git clone ${repo_url} --depth=1 ${install_name}
    fi
    cd ${install_name}/install
fi

echo "{\"install\":\"docker\"}" > install.lock

./initialization.sh
cd ..
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json
if [ ! -f "./docker-compose.yml" ]; then
    cp -i ./example/docker-compose.yml ./docker-compose.yml
fi
cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it --rm -v \$(pwd):/home/silverblog --name="silverblog_manage" silverblog/silverblog python3 manage.py \$@
EOF
chmod +x manage.sh
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "./manage.sh setting"