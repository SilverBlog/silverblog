#!/usr/bin/env bash

echo "Installing Dependency..."

if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog
fi

cat << EOF >./start.sh
#!/usr/bin/env bash
docker run -t -i -v $x:/home/SilverBlog -p 5000:5000 silverblog uwsgi --json /home/SilverBlog/uwsgi.json --chdir /home/SilverBlog
EOF
cat << EOF >./control-start.sh
#!/usr/bin/env bash
docker run -t -i -v $x:/home/SilverBlog -p 5001:5001 silverblog uwsgi --json /home/SilverBlog/uwsgi.json:control --chdir /home/SilverBlog
EOF

./install.sh

sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json





echo "The installation is complete! Please edit $x/config/system.json file."