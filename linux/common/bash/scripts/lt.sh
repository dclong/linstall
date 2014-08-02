#!/usr/bin/env bash

function lt.usage(){
    cat << EOF
Description
Syntax: lt
EOF
}

function lt(){
    if [ "$1" == "-h" ]; then
        lt.usage
        return 0
    fi
    path=$(readlink -f "$1")
    if [[ -f "$path" ]]; then
        cat "$path"
    else
        ls "$path"
    fi    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    lt $@
fi
