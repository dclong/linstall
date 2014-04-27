#!/bin/bash

function linstall.ibus.usage(){
    cat << EOF
Install ibus and ibus-sunpinyin.
Syntax: linstall.ibus
EOF
}

function linstall.ibus(){
    if [ "$1" == "-h" ]; then
        linstall.ibus.usage
        return 0
    fi
    # install ibus and ibus-sunpinyin
    wajig install -y ibus ibus-sunpinyin
    linfig.ibus
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.ibus $@
fi
