#!/bin/bash

function open.usage(){
    cat << EOF
Open Windows Explorer
Usage: open [-help] [path]
[path]: folder at which to open Windows Explorer, 
will default to current dir if not supplied.
[-help] Display help (this message).
EOF
}

function open(){
    location="${1}"
    if [ "$location" == "--help" ] || [ "$location" == "-h" ]; then
        open.usage
        return 0
    fi
    if [ "$location" == "" ]; then
        location="~"
    fi
    # check if the path exists
    if [ -e "$location" ]; then
        WIN_PATH=`cygpath -w -a "${location}"`
        cmd /C start "" "$WIN_PATH"
    else
        echo ${location} does not exist!
        return 2
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    open $@
fi
