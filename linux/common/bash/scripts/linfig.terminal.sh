#!/bin/bash

function linfig.terminal.usage(){
    echo "Configure terminal."
    echo "Syntax: linfig.jabref"
    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
}

function linfig.terminal() {
    echo "Configuring terminal ..."
    local desdir="$HOME/.config/Terminal/"
    linfig.mkdir "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then
        linfig.symlink "$lommon/terminal/terminalrc" "$desdir/terminalrc"
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.terminal $@
fi
