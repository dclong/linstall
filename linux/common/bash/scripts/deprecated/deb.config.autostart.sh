#!/bin/bash

function deb.config.autostart() {
    # need 1 argument
    # $1 the name of the autostart configuration to be linked into $HOME/.config/autostart
    echo "Configuring auto start programs ..."
    local desdir="$HOME/.config/"
    deb.config.mkdir "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then
        deb.config.symlink "$lommon/autostart/$1" "$desdir/autostart/$1"
    fi
}
