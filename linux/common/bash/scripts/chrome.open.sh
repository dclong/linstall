#!/bin/bash

function chrome.open.usage(){
    cat << EOF
Open multiple links (define in a file with a line for each link) in Google Chrome.
Syntax: chrome.open file_contains_links
EOF
}

function chrome.open(){
    if [ "$1" == "-h" ]; then
        chrome.open.usage
        return 0
    fi
    cat $1 | xargs google-chrome
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    chrome.open $@
fi
