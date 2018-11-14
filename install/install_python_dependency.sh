#!/usr/bin/env bash

if test $(ps h -o comm -p $$) = "sh"; then
    echo "Please use bash to execute this script."
    exit 1
fi

use_user=""

if [[ $UID -ne 0 ]]; then
    use_user="--user"
fi

python3 -m pip install ${use_user} -U pip

python3 -m pip install ${use_user} -U Flask hoedown xpinyin pyrss2gen gitpython requests watchdog
