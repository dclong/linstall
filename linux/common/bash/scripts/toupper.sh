#!/usr/bin/env bash

function toupper.usage(){
    cat << EOF
Change input string to upper case.
Syntax: toupper "str"
EOF
}

function toupper(){
    if [ "$1" == "-h" ]; then
        toupper.usage
        return 0
    fi
    echo "$@" | tr '[:lower:]' '[:upper:]'
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    toupper "$@"
fi
