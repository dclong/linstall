#!/bin/bash

function linux.config.ultisnips.usage(){
    cat << EOF
Configures the vim addon UltiSnips.
A symbolic link "$HOME/.vim/vim-addons/UltiSnips/UltiSnips" pointing to "$lommon/vim/UltiSnips" is created.
Syntax: linux.config.ultisnips
EOF
}

function linux.config.ultisnips(){
    if [ "$1" == "-h" ]; then
        linux.config.ultisnips.usage
        return 0
    fi
    local srcfile="$lommon/vim/UltiSnips"
    local desfile="$HOME/.vim/vim-addons/UltiSnips/UltiSnips"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.ultisnips $@
fi
