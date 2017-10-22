#!/usr/bin/env bash
pip3 install watchdog
cd ..
cat << EOF >/etc/systemd/system/silverblog.service
[Unit]
Description=SilverBlog server daemon

[Service]
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 watch.py
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -INT \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat << EOF >/etc/systemd/system/silverblog_control.service
[Unit]
Description=SilverBlog server daemon

[Service]
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/uwsgi --json ./uwsgi.json:control
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -INT \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable silverblog
systemctl enable silverblog_control