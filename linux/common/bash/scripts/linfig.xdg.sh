#!/usr/bin/env bash

function linfig.xdg.usage(){
    cat << EOF
Configure xdg.
Syntax: linfig.xdg
Create symbolic link of \"$lommon/xdg/user-dirs.conf\" to \"$HOME/.config/user-dirs.conf\".
Create symbolic link of \"$lommon/xdg/user-dirs.defaults\" to \"$HOME/.config/user-dirs.defaults\".
Create symbolic link of \"$lommon/xdg/user-dirs.dirs\" to \"$HOME/.config/user-dirs.dirs\".
Remove $HOME/Desktop if exists.
Remove $HOME/Documents if exists.
Remove $HOME/Music if exists.
Remove $HOME/Public if exists.
Remove $HOME/Templates if exists.
Remove $HOME/Videos if exists.
EOF
}

function linfig.xdg(){
    echo "Configuring xdg ..."
    local desdir="$HOME/.config"
    mkdir -p "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then
        ln -svf "$lommon/xdg/user-dirs.conf" "$desdir"
        ln -svf "$lommon/xdg/user-dirs.defaults" "$desdir"
        ln -svf "$lommon/xdg/user-dirs.dirs" "$desdir"
    fi
    # remove directoris
    rmdir "$HOME/Desktop"
    rmdir "$HOME/Documents"
    rmdir "$HOME/Music"
    rmdir "$HOME/Public"
    rmdir "$HOME/Pictures"
    rmdir "$HOME/Templates"
    rmdir "$HOME/Videos"
    if [ -d "$HOME/Downloads" ]; then
        mv "$HOME/Downloads" "$HOME/downloads"
    fi
#    mkdir -p "$HOME/archives"
    mkdir -p "$HOME/bin"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.xdg $@
fi
