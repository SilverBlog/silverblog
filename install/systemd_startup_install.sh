#!/usr/bin/env bash
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi
${use_superuser} pip3 install watchdog
if [ $(basename `pwd`) == "install" ];then
    cd ..
fi
${use_superuser} cat << EOF >/etc/systemd/system/silverblog.service
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

${use_superuser} cat << EOF >/etc/systemd/system/silverblog_control.service
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

${use_superuser} systemctl daemon-reload
${use_superuser} systemctl enable silverblog
${use_superuser} systemctl enable silverblog_control