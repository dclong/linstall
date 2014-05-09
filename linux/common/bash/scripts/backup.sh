#!/bin/bash

function backup.usage(){
    cat << EOF
Description
Syntax: backup src_dir des_dir
EOF
}

function backup(){
    if [ "$1" == "-h" ]; then
        backup.usage
        return 0
    fi
    echo "Backing up directory \"$1\" ..."
    rsync -a "$1" "$2/$(basename $1)_$(date +%Y%m%d)"    
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    backup $@
fi