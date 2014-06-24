#!/usr/bin/env bash

function trash.usage(){
    cat << EOF
Description
Syntax: trash path
EOF
}

function trash(){
    if [ "$1" == "-h" ]; then
        trash.usage
        return 0
    fi
    mkdir -p "$trash_dir"
    # if running under MobaXterm in Windows as a virtualization solutions
    if [[ "$(uname -a)" == CYGWIN_NT*GNU/Linux ]]; then
        mv $@ "$trash_dir"
        return $?
    fi
    mv -b $@ "$trash_dir"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    trash $@
fi
