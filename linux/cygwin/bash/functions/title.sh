#!/bin/bash

function title.usage(){
    cat << EOF
Set the title of Cygwin terminal.
Syntax: title [title]
EOF
}

function title(){
    local title="$(cygpath -m $(pwd))"
    if [ "$#" -ne 0 ]; then
        title="$@"
    fi
    echo -ne "\033]2;"$title"\007"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    title $@
fi
