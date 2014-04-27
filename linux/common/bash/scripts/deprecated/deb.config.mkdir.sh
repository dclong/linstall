#!/bin/bash

function deb.config.mkdir.usage(){
    cat << EOF
Make a directory in a safe mannaer.
Syntax: deb.config.mkdir path [command_prefix]
command_prefix can be "sudo" or "sudo -u user" so that you run commands with super permission.
EOF
}

function deb.config.mkdir() {
    prefix=""
    if [ "$#" -eq 2 ]; then 
        prefix="$2"
    elif [ "$#" -ne 1 ]; then
        echo "Wrong number of arguments!"
        return 1
    fi
    if [ ! -e "$1" ]; then
        echo "Creating directory \"$1\" ..."
        $prefix mkdir -p "$1"
        return 0
    fi
    if [ ! -d "$1" ]; then
        echo "A non-directory file \"$1\" exists!"
        return 1
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    deb.config.mkdir $@
fi
