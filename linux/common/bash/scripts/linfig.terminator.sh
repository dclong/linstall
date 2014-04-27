#!/bin/bash

function linfig.terminator.usage(){
    echo "Configure terminator."
    echo "Syntax: linfig.jabref"
    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
}

function linfig.terminator(){
    echo "Configuring terminator ..."
    local desdir="$HOME/.config/terminator/"
    mkdir -p "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then
        ln -svf "$lommon/terminator/config" "$desdir"
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.terminator $@
fi
