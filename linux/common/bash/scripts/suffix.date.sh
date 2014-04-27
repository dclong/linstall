#!/bin/bash
function suffix.date.usage(){
    echo "Suffix date (of format YYYYMMDD) to arguments."
    echo "Syntax: suffix.date arg1 [arg2] ..."
}
function suffix.date(){
    if [ "$1" == "-h" ]; then
        suffix.date.usage
        return 0
    fi
    for f in "$@"; do
        mv ${f} ${f}_$(date +%Y%m%d)
    done
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    suffix.date $@
fi
