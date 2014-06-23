#!/usr/bin/env bash

function 5.usage(){
    cat << EOF
Description
Syntax: 5
EOF
}

function 5(){
    if [ "$1" == "-h" ]; then
        5.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    5 $@
fi
