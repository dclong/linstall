#!/usr/bin/env bash

function 8.usage(){
    cat << EOF
Description
Syntax: 8
EOF
}

function 8(){
    if [ "$1" == "-h" ]; then
        8.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    8 $@
fi
