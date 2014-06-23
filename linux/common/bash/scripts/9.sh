#!/usr/bin/env bash

function 9.usage(){
    cat << EOF
Description
Syntax: 9
EOF
}

function 9(){
    if [ "$1" == "-h" ]; then
        9.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    9 $@
fi
