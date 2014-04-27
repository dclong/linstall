#!/bin/bash

function linfig.vimperator(){
    echo "Configuring vimperator ..."
    srcdir="$config_root_dir/common/firefox/vimperator"
    srcfile="$srcdir/vimperatorrc"
    desfile="$HOME/.vimperatorrc"
    ln -Tsvf "$srcfile" "$desfile"
    local srcdir="$srcdir/vimperator"
    ln -Tsvf "$srcdir" "$HOME/.vimperator"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.vimperator $@
fi
