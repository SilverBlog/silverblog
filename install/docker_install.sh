#!/usr/bin/env bash
docker pull qwe7002/silverblog
if [ ! -f "install.sh" ]; then
    git clone https://github.com/SilverBlogTeam/SilverBlog.git
    cd SilverBlog/install
fi

./install.sh

cd ..

cat << EOF >start.sh
#!/usr/bin/env bash
docker run -d -v $(pwd):/home/SilverBlog -p 5000:5000 qwe7002/silverblog uwsgi --json /home/SilverBlog/uwsgi.json --chdir /home/SilverBlog --touch-reload /home/SilverBlog
docker run -d -v $(pwd):/home/SilverBlog -p 5001:5001 qwe7002/silverblog uwsgi --json /home/SilverBlog/uwsgi.json:control --chdir /home/SilverBlog --touch-reload /home/SilverBlog/control_server.py
EOF
sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json