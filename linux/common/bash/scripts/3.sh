#!/usr/bin/env bash

function 3.usage(){
    cat << EOF
Description
Syntax: 3
EOF
}

function 3(){
    if [ "$1" == "-h" ]; then
        3.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    3 $@
fi
