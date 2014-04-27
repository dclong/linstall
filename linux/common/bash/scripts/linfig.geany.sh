#!/bin/bash

function linfig.geany.usage(){
    cat << EOF
Configures the Geany editor. 
A symbolic link of \"$config_root_dir/common/geany\" is made to \"$HOME/.config/geany\".
Syntax: linfig.geany
EOF
}

function linfig.geany(){
    if [ "$1" == "-h" ]; then
        linfig.geany.usage
        return 0
    fi
    local srcfile="$config_root_dir/common/geany"
    local desfile="$HOME/.config/geany"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.geany $@
fi
