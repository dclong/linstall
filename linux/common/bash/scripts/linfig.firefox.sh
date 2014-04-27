#!/bin/bash

function linfig.firefox.usage(){
    cat << EOF
Configure firefox.
Syntax: linfig firefox
Make a symbolic link of firefox (installed in /usr/local/) to /usr/bin/firefox
EOF
}

function linfig.firefox(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            echo "Configuring firefox ..."
            # symbolic link
            local desfile=/usr/bin/firefox
            local srcfile=/opt/firefox/firefox
            sudo ln -svf "$srcfile" "$desfile" 
            # desktop file
            echo "Adding firefox.desktop into /usr/share/applications/ ..."
            # move to /usr/share/applications
            local desfile="/usr/share/applications/firefox.desktop"
            sudo -u root cp "$lommon/applications/firefox.desktop" "$desfile"
            sudo -u root chmod 644 "$desfile"
            echo "Done."
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
    linfig.firefox $@
fi

