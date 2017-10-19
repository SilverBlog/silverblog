#!/usr/bin/env bash
pip3 install watchdog
cd ..
cat << EOF >/etc/systemd/system/silverblog.service
[Unit]
Description=SilverBlog server daemon

[Service]
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 watch.py
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable silverblog