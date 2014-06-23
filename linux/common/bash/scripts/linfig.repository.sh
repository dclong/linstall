#!/usr/bin/env bash
function linfig.respository.usage(){
    echo "Configure apt-get source repository."
    echo "Syntax: linfig aptget"
    echo -e "Make a symbolic link of \"$debian_dir/apt/sources.list\" \
        to /etc/apt/sources.list."
}
function linfig.repository(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            echo "Configuring Debian package repository ..."
            local srcfile=$debian_dir/apt/sources.list
            local desfile=/etc/apt/sources.list
            sudo -u root cp -f "$srcfile" "$desfile"
            local srcfile=$debian_dir/apt/preferences
            local desfile=/etc/apt/preferences
            sudo -u root cp -f "$srcfile" "$desfile"
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
    linfig.repository $@
fi
