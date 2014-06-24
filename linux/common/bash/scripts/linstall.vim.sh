#!/usr/bin/env bash

function linstall.vim.usage(){
    cat << EOF
Install the version of vim with extended supports.
Syntax: linstall.vim
EOF
}

function linstall.vim(){
    if [ "$1" == "-h" ]; then
        linstall.vim.usage
        return 0
    fi
    # install vim
    wajig install -y vim-nox vim-gui-common
    linfig.vim
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.vim $@
fi
