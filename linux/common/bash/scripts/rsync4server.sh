#!/bin/bash
function rsync4server.usage(){
    echo "Sync files from server to local."
    echo "Syntax: rsync4server server port remote_file local_file [options]"
}
function rsync4server(){
    if [ "$1" == "-h" ]; then
        rsync4server.usage
        return 0
    fi
    if [ "$#" -lt 4 ]; then
        echo "Too few arguments."
        return 0
    fi
    if [ "$#" -eq 4 ]; then
        options=""
    else
        options="$5"
    fi
    rsync -e "ssh -p $2" -azh --progress $1:"$3" "$4" $5
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    rsync4server $@
fi
