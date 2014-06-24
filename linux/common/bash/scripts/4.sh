#!/usr/bin/env bash

function 4.usage(){
    cat << EOF
Description
Syntax: 4
EOF
}

function 4(){
    if [ "$1" == "-h" ]; then
        4.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    4 $@
fi
