#!/bin/bash

function settitle.usage(){
    cat << EOF
Set the title of Cygwin terminal.
Syntax: settitle [title]
EOF
}

function settitle(){
    local title="$(cygpath -m $(pwd))"
    if [ "$#" -ne 0 ]; then
        title="$1"
    fi
    echo -ne "\033]2;"$title"\007"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    settitle $@
fi
