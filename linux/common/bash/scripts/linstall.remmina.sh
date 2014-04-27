#!/bin/bash

function linstall.remmina.usage(){
    cat << EOF
Description
Syntax: linstall.remmina
EOF
}

function linstall.remmina(){
    if [ "$1" == "-h" ]; then
        linstall.remmina.usage
        return 0
    fi
    wajig install remmina remmina-plugin-rdp   
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.remmina $@
fi
