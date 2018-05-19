#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

if [ ! -n "$1" ] ;then
    echo "you have not input username."
    exit 1
fi

install_name="silverblog"
if [ -n "$2" ];then
    install_name=$2
fi

if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    exit 1
fi

if [ -f "initialization.sh" ]; then
    cd ..
fi

if [  -f "/etc/systemd/system/silverblog.service" ]; then
    rm /etc/systemd/system/silverblog.service
fi

if [  -f "/etc/systemd/system/silverblog_control.service" ]; then
    rm /etc/systemd/system/silverblog_control.service
fi

cat << EOF >/etc/systemd/system/${install_name}@.service
[Unit]
Description=${install_name} server daemon

[Service]
User=$1
Group=$1
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 watch.py --%i
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -INT \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF


systemctl daemon-reload
systemctl enable ${install_name}@main
systemctl enable ${install_name}@control
systemctl start ${install_name}@main
systemctl start ${install_name}@control
