#!/usr/bin/env bash

function linfig.synaptics(){
    echo "Configuring touchpad ..."
    desdir="/etc/X11/xorg.conf.d"
    desfile="$desdir/10-synaptics.conf"
    srcfile="$lommon/synaptics/10-synaptics.conf"
    sudo mkdir -p "$desdir" 
    local state=$?
    if [ $state -eq 0 ]; then
        if [ -f "$desfile" ]; then
            cp "$desfile" "${srcfile}.bak"
        fi
        sudo cp -i "$srcfile" "$desfile" 
        sudo chmod 644 "$desfile"
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.synaptics $@
fi
