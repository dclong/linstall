#!/bin/bash
function cs.usage(){
    echo "Enter a directory and display its content."
    echo "Syntax: cs dir"
}
function cs(){
    if [ "$1" == "-h" ]; then
        cs.usage
        return 0
    fi
    cd "$@" 
    ls --color=auto
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    cs $@
fi
