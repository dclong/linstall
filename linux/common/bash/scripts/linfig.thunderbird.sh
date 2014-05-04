#!/bin/bash

function linfig.thunderbird.usage(){
    cat << EOF
Configure thunderbird.
Syntax: linfig thunderbird or deb.config.thunderbird
Make a symbolic link of firefox (installed in /usr/local/) to /usr/bin/firefox
EOF
}
function linfig.thunderbird(){
# I don't think try to sync tb automatically is a good idea!!!
# You should do this manually!!!
# Do every main change, setup on the main computer!
# Regularly copy your tb profile from you main computer 2 other computers.
# You can use btsync to sync thunderbird backups
# just make sure they the same!!! compare directories on 2 computers!
# keep only 3 folders at the most!!!
#-------------------------------------------------------------------------
# do more about user.js, prefs.js
# delete extensions.ini, extensions.cache and extensions.rdf
# or you probably don't need to do that
# generally speaking, don't need to sync extensions 
# unless ...
# abook.mab and history.mab
# for other address books, you'll need extra work
# persdict.dat
# Local Folders in Mail
# msgFilterRules.dat
# training.dat
# mimeTypes.rdf
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            echo "Configuring thunderbird ..."
            # symbolic link binary
            local srcfile=/opt/thunderbird/thunderbird
            local desfile=/usr/bin/thunderbird
            sudo ln -svf "$srcfile" "$desfile" 
#            srcfile="$config_root_dir/common/thunderbird"
#            desfile=~/.thunderbird
#            rm -rf "$desfile"
#            ln -svf "$srcfile" "$desfile" 
            # desktop file
            echo "Adding thunderbird.desktop into /usr/share/applications/ ..."
            # move to /usr/share/applications
            local desfile="/usr/share/applications/thunderbird.desktop"
            sudo -u root cp "$lommon/applications/thunderbird.desktop" "$desfile"
            sudo -u root chmod 644 "$desfile"
            echo "Done."
            return 0
            ;;
        *LMDE* )
            return 0
            ;;
        *Ubuntu* )
            return 0
            ;;
        * )
            echo "This script does not support ${dist:13}."
            return 1
            ;;
    esac
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.thunderbird $@
fi
