#!/usr/bin/env bash

function linfig.tcpd.usage(){
    echo "Configure tcpd."
    echo "Syntax: linfig.tcpd"
    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
}

function linfig.tcpd() {
    echo "Configuring tcpd ..."
    desfile="/etc/hosts.allow"
    srcfile="$lommon/tcpd/hosts.allow"
    if [ -f "$desfile" ]; then
        cp "$desfile" "${srcfile}.bak"
    fi
    sudo cp -i "$srcfile" "$desfile" 
    sudo chmod 644 "$desfile" 
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.tcpd $@
fi
