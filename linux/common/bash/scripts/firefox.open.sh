#!/bin/bash

function firefox.open.usage(){
    cat << EOF
Open multiple links (define in a file with a line for each link) in Firefox.
Syntax: firefox.open file_contains_links
EOF
}

function firefox.open(){
    if [ "$1" == "-h" ]; then
        firefox.open.usage
        return 0
    fi
    cat $1 | xargs firefox
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    firefox.open $@
fi
