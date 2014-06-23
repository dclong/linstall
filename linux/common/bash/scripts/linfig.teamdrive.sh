#!/usr/bin/env bash

function linfig.teamdrive.usage(){
    cat << EOF
Description
Syntax: linfig.teamdrive
EOF
}

function linfig.teamdrive(){
    if [ "$1" == "-h" ]; then
        linfig.teamdrive.usage
        return 0
    fi
    sudo ln -svf "$common/teamdrive/teamdrive.fsfilter" /etc
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.teamdrive $@
fi
