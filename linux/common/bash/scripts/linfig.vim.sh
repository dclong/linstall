#!/bin/bash

function linfig.vim.usage(){
    cat << EOF
Configure vim.
Syntax: linfig.vim
Make a symbolic link of \"$lommon/vim/vimrc/vimrc\" to \"$HOME/.vimrc\".
Make a symbolic link of \"$lommon/vim/colors\" to \"$HOME/.vim/colors\".
EOF
}
function linfig.vim(){
    echo "Configuring Vim ..."
    desfile="$HOME/.vimrc"
    srcfile="$lommon/vim/vimrc/vimrc"
    ln -Tsvf "$srcfile" "$desfile"
    local desdir="$HOME/.vim"
    mkdir -vp "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then
        ln -svf "$lommon/vim/colors" "$desdir"
        ln -svf "$lommon/vim/my_snippets" "$desdir" 
    fi
    # make a directory for SWap and backUP files
    mkdir -vp "$desdir/swup"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.vim $@
fi
