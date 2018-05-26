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

docker_image="silverblog/silverblog"
repo_url=https://github.com/SilverBlogTeam/SilverBlog.git

if [ -n ${china_install} ];then
    docker_image="registry.cn-hangzhou.aliyuncs.com/silverblog/silverblog"
    repo_url=https://gitee.com/qwe7002/silverblog.git
fi

if [ ! -f "initialization.sh" ]; then
    if [ ! -d ${install_name} ]; then
        echo "Cloning silverblog..."
        git clone ${repo_url} --depth=1 ${install_name}
    fi
    cd ${install_name}
    git fetch
    cd install
fi

echo "{\"install\":\"docker\"}" > install.lock

./initialization.sh
cd ..
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

if [ ! -f "./docker-compose.yml" ]; then
cat << EOF > docker-compose.yml
version: '3'
services:
  ${install_name}:
    image: "${docker_image}"
    tty: true
    container_name: "${install_name}"
    restart: on-failure:10
    command: python3 watch.py
    volumes:
     - $(pwd):/home/silverblog/
    ports:
     - "127.0.0.1:5000:5000"
  ${install_name}_control:
    image: "${docker_image}"
    tty: true
    container_name: "${install_name}_control"
    restart: on-failure:10
    command: python3 watch.py --control
    volumes:
     - $(pwd):/home/silverblog/
    ports:
     - "127.0.0.1:5001:5001"
EOF
fi

cat << EOF >manage.sh
#!/usr/bin/env bash
docker run -it --rm -v \$(pwd):/home/silverblog --name="${install_name}_manage" silverblog/silverblog python3 manage.py \$@
EOF
chmod +x manage.sh
echo "Before you start SilverBlog for the first time, run the following command to initialize the configuration:"
echo "./manage.sh setting"
echo "You can add the following code to .bashrc to quickly launch SilverBlog."
echo "alias ${install_name}=\"bash -c 'cd $(pwd)&&./manage.sh'\""