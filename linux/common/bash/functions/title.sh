#!/bin/bash

function title.usage(){
    cat << EOF
Set the title of Cygwin terminal.
Syntax: title [title]
EOF
}

function title(){
    # if running in Windows as a virtualization solutions
    if [[ "$(uname -a)" == CYGWIN_NT* ]]; then
        local title="$(cygpath -m $(pwd))"
    else
        local title="$(pwd)"
    fi
    title="$(basename "$title")"
    if [ "$#" -ne 0 ]; then
        title="$@"
    fi
    echo -ne "\033]2;"$title"\007"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    title $@
fi
