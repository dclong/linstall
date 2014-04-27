#!/bin/bash
function linfig.tmux.usage(){
    echo "Configure tmux."
    echo "Syntax: linfig.jabref"
    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
}

function linfig.tmux() {
    echo "Configuring tmux ..."
    linfig.symlink "$lommon/tmux/tmux.conf" "$HOME/.tmux.conf"
    echo "Done."
}


if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.tmux $@
fi
