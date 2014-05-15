#!/bin/bash

function 1.usage(){
    cat << EOF
Description
Syntax: 1
EOF
}

function 1(){
    if [ "$1" == "-h" ]; then
        1.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    1 $@
fi
