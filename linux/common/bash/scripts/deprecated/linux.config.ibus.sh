#!/bin/bash

function linux.config.ibus.usage(){
    cat << EOF
Configues IBus.
Syntax: linux.config.ibus
EOF
}

function linux.config.ibus(){
    if [ "$1" == "-h" ]; then
        linux.config.ibus.usage
        return 0
    fi
    local srcfile="$lommon/autostart/ibus_conf.desktop"
    local desfile="$HOME/.config/autostart/ibus_conf.desktop"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.ibus $@
fi
