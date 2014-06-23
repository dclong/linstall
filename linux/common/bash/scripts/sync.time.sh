#!/usr/bin/env bash
function synctime.usage(){
    echo "Sync system clock."
    echo "Syntax: synctime"
}
function synctime(){
    if [ "$1" == "-h" ]; then
        synctime.usage
        return 0
    fi
    sudo /usr/sbin/ntpdate-debian
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    sync.time $@
fi
