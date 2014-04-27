#!/bin/bash

function linfig.autostart.usage(){
    cat << EOF
Configures programs to run automatically at startup.
Syntax: linfig.autostart
EOF
}

function linfig.autostart(){
    if [ "$1" == "-h" ]; then
        linfig.autostart.usage
        return 0
    fi
    local srcdir="$lommon/autostart" 
    local desdir="$HOME/.config/autostart"
    autostart.add autolock bitsync ibus_conf terminator
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.autostart $@
fi
