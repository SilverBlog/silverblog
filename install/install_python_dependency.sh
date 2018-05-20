#!/usr/bin/env bash

use_superuser=""

if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

${use_superuser} /usr/bin/python3 -m pip install -U pip

${use_superuser} /usr/bin/python3 -m pip install -U Flask hoedown xpinyin pyrss2gen gitpython requests watchdog
