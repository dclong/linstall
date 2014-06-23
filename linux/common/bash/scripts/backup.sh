#!/usr/bin/env bash

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
    rsync -avh "$1/" "$2_$(date +%Y%m%d)"    
    # remove old backups if specified
    if [ "$#" -gt 2 ]; then
        local copies=($(ls -d "$2_"*))
        local n=${#copies[@]}
        for (( i = 0; i < $n - $3; i++ )); do
            #statements
            echo "Removing \"${copies[$i]}\" ..."
            rm -rf "${copies[$i]}"
        done
    fi
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    backup $@
fi
