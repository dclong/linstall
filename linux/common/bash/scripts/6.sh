#!/usr/bin/env bash

function 6.usage(){
    cat << EOF
Description
Syntax: 6
EOF
}

function 6(){
    if [ "$1" == "-h" ]; then
        6.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    6 $@
fi
