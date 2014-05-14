#!/bin/bash

function dl.config.usage(){
    cat << EOF
Description
Syntax: dl.config
EOF
}

function dl.config(){
    if [ "$1" == "-h" ]; then
        dl.config.usage
        return 0
    fi
    local dir=$(mktemp -d)
    cd "$dir"
    wget --no-check-certificate --load-cookies=/home/mobaxterm/ff_cookies.txt -p https://bitbucket.org/dclong/config/get/master.zip
    unzip bitbucket.org/dclong/config/get/master.zip
    cp -r dclong-config-* ~/config
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    dl.config $@
fi
