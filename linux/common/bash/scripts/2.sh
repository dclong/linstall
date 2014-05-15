#!/bin/bash

function 2.usage(){
    cat << EOF
Description
Syntax: 2
EOF
}

function 2(){
    if [ "$1" == "-h" ]; then
        2.usage
        return 0
    fi
    
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    2 $@
fi
