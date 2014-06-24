#!/usr/bin/env bash

function linfig.zim.usage(){
    cat << EOF
Description
Syntax: linfig.zim
EOF
}

function linfig.zim(){
    if [ "$1" == "-h" ]; then
        linfig.zim.usage
        return 0
    fi
    ln -Tsvf $common/zim/notes $HOME/.zim
    ln -Tsvf $common/zim/config $HOME/.config/zim
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.zim $@
fi
