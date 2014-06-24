#!/usr/bin/env bash

function caps2escape.usage(){
    cat << EOF
Map the CapsLock key to the Escape key.
Syntax: caps2escape
EOF
}

function caps2escape(){
    if [ "$1" == "-h" ]; then
        caps2escape.usage
        return 0
    fi
    setxkbmap -option -option caps:escape    
    echo "The CapsLock key is mapped to the Escape key (all previous mapping are reset)."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    caps2escape $@
fi
