#!/usr/bin/env bash
set -o errexit

bash /home/silverblog/install/initialization.sh
sed -i '''s@./config/unix_socks/main.sock@0.0.0.0:5000@g' uwsgi.json
sed -i '''s@./config/unix_socks/control.sock@0.0.0.0:5001@g' uwsgi.json
cp -rf /home/silverblog/.develop/demo/config /home/silverblog/
cp -rf /home/silverblog/.develop/demo/document /home/silverblog/
python3 manage.py update
cd /home/silverblog/templates
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"
cd /home/silverblog/
cat << EOF >supervisor.conf
[supervisord]
nodaemon=true

[program:main]
command=/home/silverblog/watch.py
autorestart=true
stdout_logfile=/var/log/silverblog-main.stdout.log
stderr_logfile=/var/log/silverblog-main.stderr.log

[program:control]
command=/home/silverblog/watch.py --control
autorestart=true
stdout_logfile=/var/log/silverblog-control.stdout.log
stderr_logfile=/var/log/silverblog-control.stderr.log

EOF