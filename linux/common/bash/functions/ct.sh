#!/bin/bash
function ct.usage(){
    cat << EOF
Enter a directory and display its content.
Syntax: ct dir
EOF
}
function ct(){
    if [ "$1" == "-h" ]; then
        ct.usage
        return 0
    fi
    cd "$@"
    title "$(basename "$(pwd)")"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    ct $@
fi
