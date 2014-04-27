#!/bin/bash

function linfig.shell.usage(){
    cat << EOF
Configure shell.
Syntax: linfig.shell
Make a symbolic link of "$lommon/bash/bash.sh" to "$HOME/.bashrc".
EOF
}

function linfig.shell(){
    echo "Configuring shell ..."
    # link the common .profile
    ln -Tsvf "$lommon/profile" "$HOME/.profile"    
    # link bash
    srcfile="$bash_dir/bashrc"
    desfile="$HOME/.bashrc"
    ln -Tsvf "$srcfile" "$desfile"
    srcfile="$bash_dir/bash_profile"
    desfile="$HOME/.bash_profile"
    ln -Tsvf "$srcfile" "$desfile"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.shell $@
fi
