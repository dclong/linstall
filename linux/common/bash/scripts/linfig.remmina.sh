#!/bin/bash

function linfig.remmina.usage(){
    cat << EOF
Configure Remmina.
echo "Syntax: linfig.remmina
echo "Make a symbolic link of \"$lommon/remmina\" to \"$HOME/.remmina\".
EOF
}

function linfig.remmina(){
    echo "Configuring Remmina ..."
    local srcfile="$lommon/remmina" 
    local desfile="$HOME/.remmina"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.remmina $@
fi
