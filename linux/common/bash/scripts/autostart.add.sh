#!/usr/bin/env bash

function autostart.add.usage(){
    cat << EOF
Add an autostart entry.
Syntax: autostart.add
EOF
}

function autostart.add(){
    if [ "$1" == "-h" ]; then
        autostart.add.usage
        return 0
    fi
    local srcdir="$lommon/autostart"    
    local desdir="$HOME/.config/autostart"
    if [ "$#" -ge 1 ]; then
        for item in "$@"; do
            if [[ "$item" != *.desktop ]]; then
                item=$item.desktop
            fi
            ln -Tsvf "$srcdir/$item" "$desdir/$item"
        done
    else
        local desktops=($(ls "$srcdir"))
        local n=${#desktops[@]}
        for ((i=0; i<$n; ++i)); do
            echo "$i: ${desktops[$i]}"
        done
        read -p "(Default none): " choice
        if [ $choice != "" ]; then
            choice=${desktops[$choice]}
            local srcfile="$srcdir/$choice"
            local desfile="$desdir/$choice"
            ln -Tsvf "$srcfile" "$desfile"
        fi
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    autostart.add $@
fi
