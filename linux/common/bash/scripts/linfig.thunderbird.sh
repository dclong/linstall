#!/bin/bash

function linfig.thunderbird.usage(){
    cat << EOF
Configure thunderbird.
Syntax: linfig thunderbird or deb.config.thunderbird
Make a symbolic link of firefox (installed in /usr/local/) to /usr/bin/firefox
EOF
}
function linfig.thunderbird(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            echo "Configuring thunderbird ..."
            # symbolic link binary
            local srcfile=/opt/thunderbird/thunderbird
            local desfile=/usr/bin/thunderbird
            sudo ln -svf "$srcfile" "$desfile" 
            srcfile="$config_root_dir/common/thunderbird"
            desfile=~/.thunderbird
            rm -rf "$desfile"
            ln -svf "$srcfile" "$desfile" 
            # desktop file
            echo "Adding thunderbird.desktop into /usr/share/applications/ ..."
            # move to /usr/share/applications
            local desfile="/usr/share/applications/thunderbird.desktop"
            sudo -u root cp "$lommon/applications/thunderbird.desktop" "$desfile"
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
    linfig.thunderbird $@
fi
