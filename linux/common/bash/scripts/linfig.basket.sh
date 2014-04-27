#!/bin/bash

function linfig.basket.usage(){
    cat << EOF
Configures the notes taking program Basket.
Syntax: linfig.basket
EOF
}

function linfig.basket(){
    if [ "$1" == "-h" ]; then
        linfig.basket.usage
        return 0
    fi
    local appdir="$HOME/.kde/share/apps"
    mkdir -p $appdir
    ln -svf "$lommon/basket" "$appdir"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.basket $@
fi
