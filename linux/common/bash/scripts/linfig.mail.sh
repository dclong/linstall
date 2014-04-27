#!/bin/bash

function linfig.mail.usage(){
    cat << EOF
Config Linux mail.
A symbolic link of "$lommon/mail/current_user" is linked to "/var/mail/current_user".
Syntax: linfig.mail
EOF
}

function linfig.mail(){
    if [ "$1" == "-h" ]; then
        linfig.mail.usage
        return 0
    fi
    local srcfile="$lommon/mail/$(whoami)"
    local desfile="/var/mail/$(whoami)"
    sudo ln -Tsvf "$srcfile" "$desfile" 
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.mail $@
fi
