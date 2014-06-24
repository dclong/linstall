#!/usr/bin/env bash

function swap.caps.escape.usage(){
    cat << EOF
Swap the CapsLock key with the Escape key.
Syntax: swap.caps.escape
EOF
}

function swap.caps.escape(){
    if [ "$1" == "-h" ]; then
        swap.caps.escape.usage
        return 0
    fi
    setxkbmap -option -option caps:swapescape
    echo "The CapsLock key is swapped with the Escape key (all previous mapping are reset)."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    swap.caps.escape $@
fi
