#!/usr/bin/env bash
#NextMoe-icecat modified 20170806 03:16(Asia/Shanghai)
#Reall Computer modified 20170810 16:16(Asia/Shanghai)
echo "Installing Dependency..."
pacman -S nginx uwsgi uwsgi-plugin-python python-pip python-wheel git
pip install flask hoedown pypinyin pyrss2gen gitpython

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

./install.sh
 
