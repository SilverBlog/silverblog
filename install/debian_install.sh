#!/usr/bin/env bash

echo "Updating software source..."

apt-get update

echo "Installing Dependency..."

apt-get install -y nginx uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git
pip3 install flask hoedown pypinyin pyrss2gen gitpython

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi

cat << EOF >../start.sh
#!/usr/bin/env bash
uwsgi --json ./uwsgi.json
EOF
cat << EOF >../control-start.sh
#!/usr/bin/env bash
uwsgi --json ./uwsgi.json:control
EOF

if [ ! -f "./start.json" ]; then
    cp -i ./example/start.example.json ./start.json
fi

./install.sh