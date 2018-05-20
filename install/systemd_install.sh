#!/usr/bin/env bash
set -o errexit
if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

install_user=${USER}
if [ -n "$1" ] ;then
    install_user=$1
fi

install_name="silverblog"
if [ -n "$2" ];then
    install_name=$2
fi

use_superuser=""
if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

if [ -f "initialization.sh" ]; then
    cd ..
fi

if [  -f "/etc/systemd/system/silverblog.service" ]; then
    ${use_superuser} rm /etc/systemd/system/silverblog.service
fi

if [  -f "/etc/systemd/system/silverblog_control.service" ]; then
    ${use_superuser} rm /etc/systemd/system/silverblog_control.service
fi


${use_superuser} bash -c "cat << EOF >/etc/systemd/system/${install_name}@.service
[Unit]
Description=${install_name} server daemon

[Service]
User=${install_user}
Group=${install_user}
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 watch.py --%i
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -INT \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF
"


${use_superuser} systemctl daemon-reload
${use_superuser} systemctl enable ${install_name}@main
${use_superuser} systemctl enable ${install_name}@control
${use_superuser} systemctl start ${install_name}@main
${use_superuser} systemctl start ${install_name}@control
