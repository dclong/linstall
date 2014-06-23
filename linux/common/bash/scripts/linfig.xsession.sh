#!/usr/bin/env bash

function linfig.xsession.usage(){
    cat << EOF
Configures xsession.
A symbolic link "$HOME/.xsessionrc" pointing to "$lommon/xsession/xsessionrc" is created.
Syntax: linfig.xsession
EOF
}

function linfig.xsession(){
    if [ "$1" == "-h" ]; then
        linfig.xsession.usage
        return 0
    fi
    local srcfile="$lommon/xsession/xsessionrc"
    local desfile="$HOME/.xsessionrc"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.xsession $@
fi
