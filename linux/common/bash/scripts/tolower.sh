#!/bin/bash

function tolower.usage(){
    cat << EOF
Change input string to lower case.
Syntax: tolower "str"
EOF
}

function tolower(){
    if [ "$1" == "-h" ]; then
        tolower.usage
        return 0
    fi
    echo "$@" | tr '[:upper:]' '[:lower:]' 
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    tolower $@
fi
