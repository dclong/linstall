#!/bin/bash

function  rmdir.nest.usage(){
    cat << EOF
Remove nested empty directories.
Syntax: rmdir.nest directory
EOF
}

function rmdir.nest(){
    if [ "$1" == "-h" ]; then
        rmdir.nest.usage
    fi
    # get content
    for e in $(ls "$1"); do
        e="$1/$e"
        if [ -d "$e" ]; then
            rmdir.nest "$e"
        fi
    done
    if [ "$(ls "$1")" == "" ]; then
        rmdir "$1"
        return 0
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    rmdir.nest $@
fi
