#!/bin/bash

function 7.usage(){
    cat << EOF
Description
Syntax: 7
EOF
}

function 7(){
    if [ "$1" == "-h" ]; then
        7.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    7 $@
fi
