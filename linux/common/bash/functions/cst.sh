#!/bin/bash
function cst.usage(){
    cat << EOF
Enter a directory and display its content.
Syntax: cs dir
EOF
}
function cst(){
    if [ "$1" == "-h" ]; then
        cst.usage
        return 0
    fi
    cs $@
	title $(basename "$@")
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    cst $@
fi