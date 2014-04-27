#!/bin/bash

function linux.config.fonts.usage(){
    cat << EOF
Configure fonts.
Syntax: linux.config.fonts
Make a symbolic link of \"$lommon/fonts\" to \"$HOME/.fonts\".
EOF
}
function linux.config.fonts(){
    echo "Configuring fonts ..."
    # configuration
    ln -Tsvf "$lommon/fonts" "$HOME/.fonts"
    echo "Refreshing fonts ..."
    fc-cache
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.fonts $@
fi
