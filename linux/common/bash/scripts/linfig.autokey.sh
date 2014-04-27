#!/bin/bash

function linfig.autokey.usage(){
    cat << EOF
Configues Autokey.
Syntax: linfig.autokey
EOF
}

function linfig.autokey(){
    if [ "$1" == "-h" ]; then
        linfig.autokey.usage
        return 0
    fi
    local srcfile="$lommon/autokey/"    
    local desfile="$HOME/.config/autokey"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.autokey $@
fi
