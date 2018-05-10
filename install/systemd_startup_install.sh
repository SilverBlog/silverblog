#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    exit 1
fi

if [ -f "initialization.sh" ]; then
    cd ..
fi

cat << EOF >/etc/systemd/system/silverblog.service
[Unit]
Description=SilverBlog server daemon

[Service]
User=$1
Group=$1
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
Description=SilverBlog control server daemon

[Service]
User=$1
Group=$1
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 watch.py --control
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -INT \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable silverblog
systemctl enable silverblog_control
systemctl start silverblog
systemctl start silverblog_control