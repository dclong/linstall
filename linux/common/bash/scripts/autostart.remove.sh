#!/bin/bash

function autostart.remove.usage(){
    cat << EOF
Remove an autostart entry.
Syntax: autostart.remove
EOF
}

function autostart.remove(){
    if [ "$1" == "-h" ]; then
        autostart.remove.usage
        return 0
    fi
    local desdir="$HOME/.config/autostart"
    if [ "$#" -ge 1 ]; then
        for item in "$@"; do
            if [[ "$item" != *.desktop ]]; then
                item=$item.desktop
            fi
            rm "$desdir/$item" && echo "\"$desdir/$item\" is removed."
        done
    else
        local desktops=($(ls "$desdir"))
        local n=${#desktops[@]}
        for ((i=0; i<$n; ++i)); do
            echo "$i: ${desktops[$i]}"
        done
        read -p "(Default none): " choice
        if [ $choice != "" ]; then
            choice=${desktops[$choice]}
            local desfile="$desdir/$choice"
            rm $desfile && echo "\"$desfile\" is removed."
        fi
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    autostart.remove $@
fi
