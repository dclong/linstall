#!/usr/bin/env bash
function debian.install.0.usage(){
    cat << EOF
Installs and configures wajig and sudo.
Syntax: debian.install.0.usage
EOF
}
function linstall.0(){
        su -c "apt-get -y update && apt-get upgrade && \
        echo -e \"\nSystem is upgraded successfully.\n\" && \
        apt-get -y install -y wajig sudo && \
        echo -e \"\nwajig and sudo are installed successfully.\n\" && \
        adduser $(whoami) sudo && \
        echo -e \"\n$(whoami) is added to the sudo group.\n\""
    newgrp sudo
    echo "Logout and then login or reboot if sudo's group permission is not in effect." && sync 
}
#' need before installation
function linux.preconfig(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            # make home directory safe
            echo "Changing permission of \"$HOME\" to 700 to make it safe ..."
            chmod 700 $HOME
            # repository
            local src_sl="$debian_dir/apt/sources.list" 
            local src_pref="$debian_dir/apt/preferences" 
            local desdir="/etc/apt"
            local des_sl="$desdir/sources.list"
            local des_pref="$desdir/preferences"
            echo "Configuring repository ..."
            echo "Updating /etc/apt/sources.list to include all versions of repositories ..."
            echo "Updating /etc/apt/preferences: stable (600) > testing (300) > unstable (200) > experimental (100) ..."
            su -c 'cp "$src_sl" "$des_sl" && chmod 644 "$des_sl" && cp "$src_pref" "$des_pref" && chmod 644 "$des_pref"'
            linstall.0
            return 0;;
        *LMDE* )
            echo "Changing permission of \"$HOME\" to 700 to make it safe ..."
            chmod 700 $HOME
            return 0;;
        *Ubuntu* )
            echo "Changing permission of \"$HOME\" to 700 to make it safe ..."
            chmod 700 $HOME
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.preconfig $@
fi
