#!/usr/bin/env bash

if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

use_superuser=""

if [ $UID -ne 0 ]; then
    echo "Superuser privileges are required to run this script."
    use_superuser="sudo"
fi

${use_superuser} /usr/bin/python3 -m pip install -U pip

${use_superuser} /usr/bin/python3 -m pip install -U Flask hoedown xpinyin pyrss2gen gitpython requests watchdog
