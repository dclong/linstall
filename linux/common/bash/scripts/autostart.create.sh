#!/bin/bash

function autostart.create.usage(){
    cat << EOF
Create an new autostart entry.
Syntax: autostart.create
EOF
}

function autostart.create(){
    if [ "$1" == "-h" ]; then
        autostart.create.usage
        return 0
    fi
    cat << EOF > "$lommon/autostart/$1.desktop"
[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=Auto Lock
Comment=Automatically locks screen after login
Exec=xscreensaver-command -lock
StartupNotify=false
Terminal=false
Hidden=false
EOF
    echo "$lommon/autostart/$1.desktop is created."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    autostart.create $@
fi
