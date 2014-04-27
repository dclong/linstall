#!/bin/bash

function linfig.lightdm.usage(){
    cat << EOF
Configures the lightdm desktop manager.
A symbolic link "/etc/lightdm/lightdm.conf" pointing to "$lommon/lightdm/lightdm.conf" is created.
Syntax: linfig.lightdm
EOF
}

function linfig.lightdm(){
    if [ "$1" == "-h" ]; then
        linfig.lightdm.usage
        return 0
    fi
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            local srcfile="$lommon/lightdm/lightdm.conf"
            local desfile="/etc/lightdm/lightdm.conf"
            sudo cp -i "$srcfile" "$desfile" 
            sudo chmod 644 "$desfile"
            return 0;;
        *LMDE* )
            return 0;;
        *Ubuntu* )
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.lightdm $@
fi
